from typing import List
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.adcreative import AdCreative

class CampaignService:

    def create_campaign(self):
        
        FacebookAdsApi.init(access_token='your_facebook_access_token')
        campaign = AdAccount('act_<AD_ACCOUNT_ID>').create_campaign(
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