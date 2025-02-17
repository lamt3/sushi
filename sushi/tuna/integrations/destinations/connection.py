import requests
import datetime
from abc import ABC, abstractmethod

from tuna.config import Config

class AdToken:
    access_token: str
    expires_at: datetime

class AdOAuthService(ABC):
    @abstractmethod
    def get_auth_url(self)->str:
        pass

    @abstractmethod
    async def exchange_code_for_token(self)->AdToken:
        pass


def get_oauth_service(ad_type: str)->AdOAuthService:
    if ad_type == "fb":
        return FacebookOAuthService()
    
    return None


class FacebookOAuthService(AdOAuthService):
    AUTH_URL = "https://www.facebook.com/v18.0/dialog/oauth?"
    TOKEN_URL = "https://graph.facebook.com/v18.0/oauth/access_token"
    REFRESH_TOKEN_URL = "https://graph.facebook.com/oauth/access_token"
    REDIRECT_URI = Config.FB_REDIRECT_URI
    CLIENT_ID = Config.FB_CLIENT_ID
    CLIENT_SECRET = Config.FB_CLIENT_SECRET

    def get_auth_url(self)->str:
        """Generate Facebook OAuth authorization URL"""
        params = {
            "client_id":Config.FB_CLIENT_ID,
            "redirect_uri":  Config.FB_REDIRECT_URI,
            "scope": "ads_read,ads_management,read_insights",
            "response_type": "code",
        }
        url = requests.Request("GET", self.AUTH_URL, params=params).prepare().url
        return url

    async def exchange_code_for_token(self, code: str)->AdToken:
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

        access_token = response_data["access_token"]
        expires_in = response_data.get("expires_in", 3600)
        expires_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)

        return {"access_token": access_token, "expires_at": expires_at}

    async def refresh_token(self):
        """Refresh tokens that are near expiry"""
        # db = SessionLocal()
        # now = datetime.datetime.utcnow()
        # tokens_to_refresh = db.query(FacebookToken).filter(
        #     FacebookToken.expires_at <= now + datetime.timedelta(minutes=5)
        # ).all()

        refreshed_tokens = []
        # for token_entry in []:#tokens_to_refresh:
        #     data = {
        #         "grant_type": "fb_exchange_token",
        #         "client_id": "settings.fb_client_id",
        #         "client_secret": "settings.fb_client_secret",
        #         "fb_exchange_token": token_entry.access_token,
        #     }
        #     response = requests.get(self.REFRESH_TOKEN_URL, params=data)
        #     response_data = response.json()

        #     if "access_token" in response_data:
        #         token_entry.access_token = response_data["access_token"]
        #         expires_in = response_data.get("expires_in", 3600)
        #         token_entry.expires_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
        #         db.commit()
        #         refreshed_tokens.append(token_entry.access_token)

        # db.close()
        return refreshed_tokens











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