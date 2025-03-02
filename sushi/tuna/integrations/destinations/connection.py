import requests
import datetime
from abc import ABC, abstractmethod
from tuna.dtos.ad_dto import AdAccessToken
from tuna.config import Config
from typing import Optional

class AdOAuthClient(ABC):
    @abstractmethod
    def get_auth_url(self, callback_url)->str:
        pass

    @abstractmethod
    async def exchange_code_for_token(self)->AdAccessToken:
        pass
    
    def get_client(ad_type: str)->Optional["AdOAuthClient"]:
        if ad_type == "fb":
            return FacebookOAuthClient()
    
        return None

class FacebookOAuthClient(AdOAuthClient):
    AUTH_URL = "https://www.facebook.com/v18.0/dialog/oauth?"
    TOKEN_URL = "https://graph.facebook.com/v18.0/oauth/access_token"
    REDIRECT_URI = Config.FB_REDIRECT_URI
    CLIENT_ID = Config.FB_CLIENT_ID
    CLIENT_SECRET = Config.FB_CLIENT_SECRET

    def get_auth_url(self, callback_url)->str:
        """Generate Facebook OAuth authorization URL"""
        params = {
            "client_id":Config.FB_CLIENT_ID,
            "redirect_uri":  Config.FB_REDIRECT_URI,
            "scope": "ads_read,ads_management,read_insights",
            "response_type": "code",
            "state": callback_url
        }
        url = requests.Request("GET", self.AUTH_URL, params=params).prepare().url
        return url

    async def exchange_code_for_token(self, code: str)->AdAccessToken:
        """Exchange authorization code for access token"""
        data = {
            "client_id": Config.FB_CLIENT_ID,
            "client_secret": Config.FB_CLIENT_SECRET,
            "redirect_uri": Config.FB_REDIRECT_URI,
            "code": code,
        }
        response = requests.post(self.TOKEN_URL, data=data)
        response_data = response.json()

        if "access_token" not in response_data:
            raise Exception("Error fetching access token")
        
        short_lived_access_token = response_data["access_token"]

        long_lived_params = {
            "grant_type": "fb_exchange_token",
            "client_id": Config.FB_CLIENT_ID,
            "client_secret": Config.FB_CLIENT_SECRET,
            "fb_exchange_token": short_lived_access_token
        }
        long_lived_response = requests.get(self.TOKEN_URL, params=long_lived_params)
        long_lived_data = long_lived_response.json()

        if "access_token" not in long_lived_data:
            return Exception("Error fetching access token")
        
        access_token = long_lived_data["access_token"]
        expires_in = long_lived_data.get("expires_in")
        expires_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
        
        #note: fb doesn't provide refresh_tokens; access_tokens expires in 60 days. Can request for system user token instead in future, but more effort for user.
        return AdAccessToken(
            ad_platform_name="fb",
            access_token=access_token,
            access_token_expiry=expires_at,
            refresh_token="" 
        )
  

class TikTokOAuthClient(AdOAuthClient):
    AUTH_URL = "https://www.tiktok.com/v2/auth/authorize/"
    TOKEN_URL = "https://business-api.tiktok.com/open_api/v2/oauth/token/"
    REFRESH_URL = "https://business-api.tiktok.com/open_api/v2/oauth/refresh_token/"

    def get_auth_url(self, callback_url)->str:

        scopes = [
            "tiktok_business_ads.manage",  # Manage ads
            "tiktok_business_ads.read",    # Read ad accounts, campaigns, and ads
            "tiktok_business_creative.read",  # View creative assets
            "tiktok_business_creative.manage",  # Upload/manage creatives
            "tiktok_business_audience.read",  # Read audience data
            "tiktok_business_audience.manage",  # Create/manage custom audiences
            "tiktok_business_insights.read"  # Fetch analytics data
        ]
        
        params = {
            "client_key": Config.TIKTOK_CLIENT_ID,
            "response_type": "code",
            "scope": " ".join(scopes),  # Space-separated list of scopes
            "redirect_uri": Config.TIKTOK_REDIRECT_URI,
            "state": callback_url,
        }
    
        return requests.Request("GET", self.AUTH_URL, params=params).prepare().url 

    async def exchange_code_for_token(self, code: str)->AdAccessToken:
        """Exchange authorization code for access token"""
        payload = {
            "client_key": Config.TIKTOK_CLIENT_ID,
            "client_secret": Config.TIKTOK_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": Config.TIKTOK_REDIRECT_URI
        }
        response = requests.post(self.TOKEN_URL, json=payload)
        data = response.json()
    
        if "error_code" in data and data["error_code"] != 0:
            return {"error": data["message"]}

        return {
            "access_token": data["data"]["access_token"],
            "expires_in": data["data"]["expires_in"],
            "refresh_token": data["data"]["refresh_token"],
            "refresh_expires_in": data["data"]["refresh_expires_in"]
        }
    
    async def refresh_access_token(self, refresh_token):
        payload = {
            "client_key": Config.TIKTOK_CLIENT_ID,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        
        response = requests.post(self.REFRESH_URL, json=payload)
        data = response.json()
        
        if "error_code" in data and data["error_code"] != 0:
            return {"error": data["message"]}

        return {
            "access_token": data["data"]["access_token"],
            "expires_in": data["data"]["expires_in"],  # 1 day
            "refresh_token": data["data"]["refresh_token"],
            "refresh_expires_in": data["data"]["refresh_expires_in"]  # 30 days
        }


  






# class OAuthService:
#     @staticmethod
#     def get_tiktok_auth_url():
#         redirect_uri = "http://localhost:8000/callback/tiktok"
#         return f"https://ads.tiktok.com/marketing_api/auth?app_id={"TIKTOK_CLIENT_ID"}&redirect_uri={redirect_uri}&state=random-state"

#     @staticmethod
#     def exchange_tiktok_token(auth_code: str):
#         payload = {
#             "app_id": "TIKTOK_CLIENT_ID",
#             "secret": "TIKTOK_CLIENT_SECRET",
#             "auth_code": auth_code
#         }
#         response = requests.post("https://business-api.tiktok.com/open_api/v1.3/oauth2/access_token/", json=payload)
#         response.raise_for_status()
#         return response.json()

#     @staticmethod
#     def get_facebook_auth_url():
#         redirect_uri = "http://localhost:8000/callback/facebook"
#         scope = "ads_management,ads_read"
#         return f"https://www.facebook.com/v16.0/dialog/oauth?client_id={FACEBOOK_CLIENT_ID}&redirect_uri={redirect_uri}&scope={scope}"

#     @staticmethod
#     def exchange_facebook_token(auth_code: str):
#         params = {
#             "client_id": FACEBOOK_CLIENT_ID,
#             "client_secret": FACEBOOK_CLIENT_SECRET,
#             "redirect_uri": "http://localhost:8000/callback/facebook",
#             "code": auth_code
#         }
#         response = requests.get("https://graph.facebook.com/v16.0/oauth/access_token", params=params)
#         response.raise_for_status()
#         return response.json()

#     @staticmethod
#     def get_google_auth_url():
#         redirect_uri = "http://localhost:8000/callback/google"
#         scope = "https://www.googleapis.com/auth/adwords"
#         return f"https://accounts.google.com/o/oauth2/v2/auth?client_id={GOOGLE_CLIENT_ID}&redirect_uri={redirect_uri}&scope={scope}&response_type=code"

#     @staticmethod
#     def exchange_google_token(auth_code: str):
#         payload = {
#             "code": auth_code,
#             "client_id": GOOGLE_CLIENT_ID,
#             "client_secret": GOOGLE_CLIENT_SECRET,
#             "redirect_uri": "http://localhost:8000/callback/google",
#             "grant_type": "authorization_code"
#         }
#         response = requests.post("https://oauth2.googleapis.com/token", data=payload)
#         response.raise_for_status()
#         return response.json()

#     @staticmethod
#     def get_twitter_auth_url():
#         oauth = OAuth1Session(TWITTER_CONSUMER_KEY, client_secret=TWITTER_CONSUMER_SECRET)
#         request_token_url = "https://api.twitter.com/oauth/request_token"
#         response = oauth.fetch_request_token(request_token_url)
#         return f"https://api.twitter.com/oauth/authorize?oauth_token={response['oauth_token']}"

#     @staticmethod
#     def exchange_twitter_token(oauth_token: str, oauth_verifier: str):
#         oauth = OAuth1Session(TWITTER_CONSUMER_KEY, client_secret=TWITTER_CONSUMER_SECRET,
#                                resource_owner_key=oauth_token, verifier=oauth_verifier)
#         access_token_url = "https://api.twitter.com/oauth/access_token"
#         response = oauth.fetch_access_token(access_token_url)
#         return response