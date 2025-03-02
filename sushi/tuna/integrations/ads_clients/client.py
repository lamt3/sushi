import requests

from abc import ABC, abstractmethod

from tuna.dtos.ad_dto import AdAccount
from typing import List, Optional

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.adcreative import AdCreative

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

    def create_campaign(self, access_token, ad_account_id):
        FacebookAdsApi.init(access_token=access_token)
        campaign = AdAccount(f'act_{ad_account_id}').create_campaign(
            fields=[],
            params={
                'name': 'My First Campaign',
                'objective': 'OUTCOME_TRAFFIC',
                'status': 'PAUSED',
                'special_ad_categories': [],
            }
        )
        campaign.execute()
    
    def create_ad_set(self):
        ad_set = AdAccount("ad_account_id").create_ad_set(
        fields=[],
        params={
            'name': 'My First Ad Set',
            'campaign_id': "campaign_id",
            'daily_budget': 1000,
            'start_time': '2023-10-01T00:00:00-0700',
            'end_time': '2023-10-31T23:59:59-0700',
            'billing_event': 'IMPRESSIONS',
            'optimization_goal': 'REACH',
            'bid_strategy': 'LOWEST_COST_WITHOUT_CAP',
            'targeting': {
                'age_min': 18,
                'age_max': 65,
                'genders': [1],
                'geo_locations': {'countries': ['US']},
                'interests': [{'id': 6003139266461, 'name': 'Technology'}],
            },
            'status': 'PAUSED',
            }
        )
        ad_set_id = ad_set['id']

    def create_ad_creative(self):
        ad_creative = AdAccount("ad_account_id").create_ad_creative(
        fields=[],
        params={
            'name': 'My First Ad Creative',
            'object_story_spec': {
                'page_id': 'your_page_id',
                'link_data': {
                    'link': 'https://www.example.com',
                    'message': 'Check out this amazing product!',
                    'image_hash': 'your_image_hash',
                    },
                },
            }
        )
        ad_creative_id = ad_creative['id']


class TikTokClient(AdClient):
    BASE_URL = "https://business-api.tiktok.com/open_api/v1.3/"

    def __init__(self, access_token):
        """
        Initializes the TikTokAdClient with the provided access token.
        """
        self.access_token = access_token
        self.headers = {
            "Access-Token": self.access_token,
            "Content-Type": "application/json"
        }

    def get_ad_accounts(self):
        """
        Retrieves a list of TikTok Ad Accounts.

        Returns:
            dict: JSON response containing ad account details.
        """
        url = self.BASE_URL + "advertiser/info/"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def create_campaign(self, advertiser_id, campaign_name, objective_type, budget, budget_mode="BUDGET_MODE_INFINITE"):
        """
        Creates a TikTok Ad Campaign.

        Params:
            advertiser_id (str): TikTok Ad account ID.
            campaign_name (str): Name of the campaign.
            objective_type (str): Campaign objective. Options: ["TRAFFIC", "CONVERSIONS", "VIDEO_VIEWS", "REACH"]
            budget (float): Budget amount.
            budget_mode (str): "BUDGET_MODE_INFINITE" (no limit) or "BUDGET_MODE_DAY" (daily limit).

        Returns:
            dict: JSON response with campaign details.
        """
        url = self.BASE_URL + "campaign/create/"
        data = {
            "advertiser_id": advertiser_id,
            "campaign_name": campaign_name,
            "objective_type": objective_type,
            "budget": budget,
            "budget_mode": budget_mode
        }
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def create_adset(self, advertiser_id, campaign_id, adset_name, placement, targeting, budget, start_time, end_time, bid=0.1, bid_strategy="BID_STRATEGY_CUSTOM"):
        """
        Creates an Ad Set under a given Campaign.

        Params:
            advertiser_id (str): TikTok Ad account ID.
            campaign_id (str): Campaign ID.
            adset_name (str): Name of the Ad Set.
            placement (list): Platforms for ads (e.g., ["PLACEMENT_TIKTOK", "PLACEMENT_PANGLE"])
            targeting (dict): Targeting options (e.g., {"age": [18, 24], "gender": "FEMALE"})
            budget (float): Budget amount.
            start_time (int): Start time (Unix timestamp).
            end_time (int): End time (Unix timestamp).
            bid (float): Bid amount.
            bid_strategy (str): Bid strategy ["BID_STRATEGY_CUSTOM", "BID_STRATEGY_LOWEST_COST"]

        Returns:
            dict: JSON response with Ad Set details.
        """
        url = self.BASE_URL + "adgroup/create/"
        data = {
            "advertiser_id": advertiser_id,
            "campaign_id": campaign_id,
            "adgroup_name": adset_name,
            "placement": placement,
            "placement_type": "place",
            "interest_category_ids": ["ids"],
            "actions" : ["actions"],
            "budget_mode": "BUDGET_MODE_TOTAL",
            "budget": {{budget}},
            "schedule_type": "SCHEDULE_START_END",
            "schedule_end_time": "{{schedule_end_time}}",
            "schedule_start_time": "{{schedule_start_time}}",
            "optimization_goal": "CLICK",
            "bid_type": "BID_TYPE_NO_BID",
            "billing_event": "CPC",
            "pacing": "PACING_MODE_SMOOTH",
            "operation_status": "ENABLE"
        }
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def create_ad(self, advertiser_id, adset_id, ad_name, ad_format, creative_material_mode, video_id, call_to_action):
        """
        Creates an Ad within an Ad Set.

        Params:
            advertiser_id (str): TikTok Ad account ID.
            adset_id (str): Ad Set ID.
            ad_name (str): Name of the Ad.
            ad_format (str): Format of the Ad. Options: ["SINGLE_VIDEO", "IMAGE"]
            creative_material_mode (str): "UNION" (auto-matching) or "SINGLE" (manual selection).
            video_id (str): TikTok video ID to use in the Ad.
            call_to_action (str): Call to action. Examples: ["SHOP_NOW", "SIGN_UP", "LEARN_MORE"]

        Returns:
            dict: JSON response with Ad details.
        """
        url = self.BASE_URL + "ad/create/"
        data = {
            "advertiser_id": advertiser_id,
            "adgroup_id": adset_id,
            "ad_name": ad_name,
            "ad_format": ad_format,
            "creative_material_mode": creative_material_mode,
            "video_id": video_id,
            "call_to_action": call_to_action
        }
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()



