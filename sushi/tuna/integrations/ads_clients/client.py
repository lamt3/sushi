import requests

from abc import ABC, abstractmethod

from tuna.dtos.ad_dto import AdAccount
from typing import List, Optional

class AdClient(ABC):
    @abstractmethod
    def get_ad_accounts(self, access_token:str)->List[AdAccount]:
        pass

    @staticmethod
    def get_ad_client(ad_platform: str)->Optional["AdClient"]:
        if ad_platform == "fb":
            return FBAdClient()
        
        return None

class FBAdClient(AdClient):
    
    def get_ad_accounts(self, access_token:str)->List[AdAccount]:
         """Fetch the list of ad accounts for the authenticated user."""
         FB_AD_ACCOUNTS_URL = "https://graph.facebook.com/v18.0/me/adaccounts"
         headers = {"Authorization": f"Bearer {access_token}"}
         params = {
            "fields": "id,name,account_id,currency,status,daily_spend_limit,spend_cap,balance,amount_spent", 
        }
         response = requests.get(FB_AD_ACCOUNTS_URL, params, headers=headers)
         data = response.json()

         print(data)

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
         ad_accounts = []
         for d in data.get("data", []):
             account_id = d["id"]
             name = d.get("name", account_id)
             currency = d.get("currency", "")
             ad_account = AdAccount(
                 platform="fb",
                 account_id=account_id,
                 name=name,
                 currency=currency
             )
             ad_accounts.append(ad_account)
             
         return ad_accounts



