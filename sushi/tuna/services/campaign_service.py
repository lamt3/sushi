from typing import List
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.adcreative import AdCreative


# from sqlalchemy import (
#     Column, String, Integer, ForeignKey, Text, Table, Enum
# )
# from sqlalchemy.orm import relationship, declarative_base
# from sqlalchemy.dialects.postgresql import JSON

# Base = declarative_base()

# # Organization Table
# class Organization(Base):
#     __tablename__ = 'organizations'
    
#     id = Column(Integer, primary_key=True)
#     name = Column(String(255), nullable=False, unique=True)
    
#     ad_accounts = relationship("AdAccount", back_populates="organization")

# # Ad Platforms Enum
# from enum import Enum as PyEnum
# class AdPlatformType(PyEnum):
#     FACEBOOK = "Facebook"
#     INSTAGRAM = "Instagram"
#     TIKTOK = "TikTok"

# class AdAccount(Base):
#     __tablename__ = 'ad_accounts'

#     id = Column(Integer, primary_key=True)
#     name = Column(String(255), nullable=False)
#     platform = Column(Enum(AdPlatformType), nullable=False)
#     organization_id = Column(Integer, ForeignKey('organizations.id'))

#     organization = relationship("Organization", back_populates="ad_accounts")
#     campaigns = relationship("Campaign", back_populates="ad_account")

# class Campaign(Base):
#     __tablename__ = 'campaigns'

#     id = Column(Integer, primary_key=True)
#     name = Column(String(255), nullable=False)
#     ad_account_id = Column(Integer, ForeignKey('ad_accounts.id'))

#     ad_account = relationship("AdAccount", back_populates="campaigns")
#     ad_sets = relationship("AdSet", back_populates="campaign")

# class AdSet(Base):
#     __tablename__ = 'ad_sets'

#     id = Column(Integer, primary_key=True)
#     name = Column(String(255), nullable=False)
#     campaign_id = Column(Integer, ForeignKey('campaigns.id'))

#     campaign = relationship("Campaign", back_populates="ad_sets")
#     ad_creatives = relationship("AdCreative", back_populates="ad_set")

# class AdCreative(Base):
#     __tablename__ = 'ad_creatives'

#     id = Column(Integer, primary_key=True)
#     content = Column(Text, nullable=False)
#     images = Column(JSON, nullable=True)  # Store image URLs or paths
#     description = Column(Text, nullable=True)
#     ad_set_id = Column(Integer, ForeignKey('ad_sets.id'))

#     ad_set = relationship("AdSet", back_populates="ad_creatives")

class AdPlatformCreative: 
    name: str
    content_type: str
    image: str
    video: str

class AdSet:
    name: str
    description: str
    audience: str
    budget: str
    ad_creatives: List[AdCreative]

class AdPlatformCampaign:
    title: str
    description: str
    created_at: str
    updated_at: str
    created_by: str
    updated_by: str
    objective: str
    ad_set: List[AdSet]

class AdPlatformAccount:
    ad_platform: str
    ad_account_id: str
    name: str
    ad_campaigns: List[AdPlatformCampaign]


class SushiCampaign:
    sushi_campaign_id: str
    title: str
    description: str
    created_at: str
    updated_at: str
    created_by: str
    updated_by: str
    objective: str
    ad_campaigns: List[AdPlatformAccount]

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