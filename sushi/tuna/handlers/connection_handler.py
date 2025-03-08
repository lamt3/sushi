from tuna.services.ad_service import AdService
from tuna.integrations.destinations.connection import AdOAuthClient
from fastapi.responses import RedirectResponse
from fastapi import HTTPException
import uuid
from fastapi import Request, Query
import logging
import requests
import hmac
import hashlib
import base64
import json
import urllib.parse
import secrets
from tuna.config import Config

logger = logging.getLogger(__name__)

class ConnectionHandler:
    def __init__(self, ads: AdService):
        self.ads = ads

    def get_auth_url(self, ad_platform:str, callback_url:str):
        try:
            auth_url = self.ads.get_auth_url(ad_platform, callback_url)
            return RedirectResponse(auth_url)
        except Exception as e:
            logger.error(f"error...{str(e)}")
            # to do: redirect back to app w/ error param
            raise HTTPException(status_code=400, detail=str(e))
    
    async def get_oauth_token(self, request: Request, ad_platform:str, code: str, state: str):
        try:             
            member = request.state.member
            await self.ads.add_oauth_connection(organization_id=member["organization_id"], ad_platform=ad_platform, code=code)
            return RedirectResponse(url=state)
        except Exception as e:
            # to do: redirect back to app w/ error param
            raise HTTPException(status_code=400, detail=str(e))
        
    async def shopify_oauth(request: Request, shop: str, id_token: str):
        """Handle OAuth callback from Shopify"""
        
        try: 
            print("in shopifiy oauth...")
            # 1. Verify the HMAC signature
            # if not verify_hmac(request, Config.SHOPIFY_SECRET_KEY):
            #     raise HTTPException(status_code=403, detail="Invalid HMAC signature")
            
            # 2. Exchange code for access token
            access_token = await exchange_code_for_token(shop, id_token)
            
            # 3. Auto-register the web pixel
            await create_web_pixel(shop, access_token)
            print("successfully installed shopify oauth...")
            
            # # 4. Store shop data in your database
            # await store_shop_data(shop, access_token)
            
            # 5. Redirect back to Shopify admin
            # return RedirectResponse(url=f"https://{shop}/admin/apps")
            return RedirectResponse(url=f"https://figsprout.netlify.app/dashboard")
        except Exception as e:
            print(f"Error in shopify oauth due to {str(e)} ")
            raise HTTPException(status_code=403, detail="Shopify Login Failed. Please Try Again.")

   
# async def exchange_code_for_token(shop: str, id_token: str):
#     """Exchange authorization code for permanent access token"""
    
#     token_url = f"https://{shop}/admin/oauth/access_token"
#     payload = {
#         "client_id": Config.SHOPIFY_CLIENT_ID,
#         "client_secret": Config.SHOPIFY_SECRET_KEY,
#         "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
#         "subject_token": id_token,
#         "subject_token_type": "urn:ietf:params:oauth:token-type:id_token",
#         "requested_token_type": "urn:shopify:params:oauth:token-type:online-access-token"
#     }
    
#     response = requests.post(token_url, json=payload)
    
#     if response.status_code != 200:
#         raise Exception(f"Failed to get access token: {response.text}")
    
#     data = response.json()
#     return data.get("access_token")
    async def initiate_shopify_oauth(self, request: Request, shop: str):
        """Start Shopify OAuth process with shop parameter"""
        try:
            # Verify shop parameter is valid
            if not shop or not shop.strip():
                raise HTTPException(status_code=400, detail="Shop parameter is required")
            
            # Clean shop parameter
            shop = shop.strip()
            if not shop.endswith('myshopify.com'):
                shop = f"{shop}.myshopify.com"
            
            # Generate a nonce for security
            nonce = secrets.token_hex(16)
            
            # Build redirect URL for authorization
            redirect_uri = "https://sushi-api-951508746812.asia-southeast1.run.app/api/v1/shopify/oauth"
            scopes = "write_pixels,read_customer_events"
            
            auth_url = (
                f"https://{shop}/admin/oauth/authorize?"
                f"client_id={Config.SHOPIFY_CLIENT_ID}&"
                f"scope={scopes}&"
                f"redirect_uri={urllib.parse.quote(redirect_uri)}&"
                f"state={nonce}"
            )
            
            # Since this is a non-embedded app, we can do a direct 3xx redirect
            return RedirectResponse(url=auth_url)
            
        except Exception as e:
            print(f"Error initiating Shopify OAuth: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
    
    # Step 2: Handle OAuth callback
    async def shopify_oauth(self, request: Request, shop: str = None, code: str = None, state: str = None):
        """Handle OAuth callback from Shopify"""
        
        try: 
            print(f"In Shopify OAuth with shop: {shop}, state: {state}")
            
            # # Verify HMAC signature
            # if not verify_hmac(request, Config.SHOPIFY_SECRET_KEY):
            #     raise HTTPException(status_code=403, detail="Invalid HMAC signature")
            
            # # Validate shop parameter
            # if not shop or not is_valid_shop(shop):
            #     raise HTTPException(status_code=400, detail="Invalid shop parameter")
            
            # Exchange authorization code for access token
            access_token = exchange_code_for_token(shop, code)
            
            # Register the web pixel with the shop
            await create_web_pixel(shop, access_token)
            print("Successfully installed Shopify web pixel")
            
            # Get shop details (optional but useful)
            # shop_details = await get_shop_details(shop, access_token)
            
            # Create a secure token for verification in your app
            # token = create_secure_token(shop, shop_details)
            
            # Direct 3xx redirect to your external app
            # Include relevant shop data your app needs
            redirect_url = (
                f"https://figsprout.netlify.app/connect?"
                f"shop={shop}"
                # f"shop_name={urllib.parse.quote(shop_details.get('name', ''))}&"
                # f"email={urllib.parse.quote(shop_details.get('email', ''))}&"
                # f"token={token}"
            )
            
            # Use status_code=303 as recommended for 3xx redirects after POST
            return RedirectResponse(url=redirect_url, status_code=303)
            
        except Exception as e:
            print(f"Error in Shopify OAuth: {str(e)}")
            raise HTTPException(status_code=403, detail=f"Shopify Login Failed: {str(e)}")

# Helper functions

def verify_hmac(request: Request, api_secret: str) -> bool:
    """Verify the HMAC signature from Shopify"""
    
    # Get query parameters
    query_params = dict(request.query_params)
    hmac_value = query_params.pop("hmac", None)
    
    if not hmac_value:
        return False
    
    # Sort parameters alphabetically
    sorted_params = sorted(query_params.items())
    
    # Join parameters as key=value&key2=value2
    message = "&".join([f"{key}={value}" for key, value in sorted_params])
    
    # Create HMAC hash
    digest = hmac.new(
        api_secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    # Compare computed HMAC with provided HMAC
    return hmac.compare_digest(digest, hmac_value)

def is_valid_shop(shop: str) -> bool:
    """Validate shop parameter format"""
    import re
    pattern = r'^[a-zA-Z0-9][a-zA-Z0-9\-]*\.myshopify\.com$'
    return bool(re.match(pattern, shop))

def exchange_code_for_token(shop: str, code: str):
    """Exchange authorization code for access token"""
    url = f"https://{shop}/admin/oauth/access_token"
    
    data = {
        "client_id": Config.SHOPIFY_CLIENT_ID,
        "client_secret": Config.SHOPIFY_SECRET_KEY,
        "code": code
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code != 200:
        raise Exception(f"Failed to get access token: {response.text}")
    
    result = response.json()
    access_token = result.get("access_token")
    
    if not access_token:
        raise Exception("No access token received from Shopify")
    
    return access_token


async def create_web_pixel(shop: str, access_token: str):
    """Create a web pixel for the shop using GraphQL"""
    
    # Generate a unique account ID for this shop
    account_id = str(uuid.uuid4())
    print("registering web pixel")
    
    # GraphQL endpoint
    url = f"https://{shop}/admin/api/2023-10/graphql.json"
    
    # Headers with access token
    headers = {
        "X-Shopify-Access-Token": access_token,
        "Content-Type": "application/json"
    }
    
    # GraphQL mutation to create web pixel
    query = """
    mutation {
        webPixelCreate(webPixel: { settings: SETTINGS_JSON }) {
            userErrors {
                code
                field
                message
            }
            webPixel {
                settings
                id
            }
        }
    }
    """
    
    # Replace the settings JSON placeholder with properly escaped JSON
    settings_json = json.dumps({"accountID": account_id})
    query = query.replace("SETTINGS_JSON", json.dumps(settings_json))
    
    # Make the request
    response = requests.post(
        url,
        headers=headers,
        json={"query": query}
    )

    print(response)
    result = response.json()
    if response.status_code != 200:
        if result.get('code') == "TAKEN":
            return True
        raise Exception(f"Failed to create web pixel: {response.text}")
    
    
    
    # Check for errors in the GraphQL response
    if "errors" in result or result.get("data", {}).get("webPixelCreate", {}).get("userErrors", []):
        errors = result.get("errors") or result.get("data", {}).get("webPixelCreate", {}).get("userErrors", [])
        raise Exception(f"GraphQL errors: {errors}")
    
    # # Store account_id with shop in your database for future reference
    # await update_shop_account_id(shop, account_id)
    
    return result


# def verify_hmac(request: Request, api_secret: str) -> bool:
#     """Verify the HMAC signature from Shopify"""
    
#     # Get query parameters
#     query_params = dict(request.query_params)
#     hmac_value = query_params.pop("hmac")
    
#     # Sort parameters alphabetically
#     sorted_params = sorted(query_params.items())
    
#     # Join parameters as key=value&key2=value2
#     message = "&".join([f"{key}={value}" for key, value in sorted_params])
    
#     # Create HMAC hash
#     digest = hmac.new(
#         api_secret.encode('utf-8'),
#         message.encode('utf-8'),
#         hashlib.sha256
#     ).hexdigest()
    
#     # Compare computed HMAC with provided HMAC
#     return hmac.compare_digest(digest, hmac_value)