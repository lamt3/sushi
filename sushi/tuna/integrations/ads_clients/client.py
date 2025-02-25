import requests

from abc import ABC, abstractmethod

class AdClient(ABC):
    @abstractmethod
    def get_ad_accounts(self, access_token:str):
        pass

class FBAdClient(AdClient):
    FB_API_URL = "https://graph.facebook.com/v18.0/me/adaccounts"
    def get_ad_accounts(self, access_token:str):
         """Fetch the list of ad accounts for the authenticated user."""
         headers = {"Authorization": f"Bearer {access_token}"}
         response = requests.get(self.FB_API_URL, headers=headers)
         data = response.json()

         if "error" in data:
            return {"error": data["error"]["message"]}
         
#          {
#   "data": [
#     {
#       "id": "act_123456789",
#       "account_id": "123456789",
#       "name": "My Ad Account",
#       "currency": "USD",
#       "account_status": 1
#     }
#   ]
# }
         
#          {
#   "error": {
#     "message": "Invalid OAuth access token.",
#     "type": "OAuthException",
#     "code": 190
#   }
# }

         return data.get("data", [])



