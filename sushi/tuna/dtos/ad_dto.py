from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from enum import Enum

class AdAccessToken(BaseModel):
    ad_platform_name: str
    access_token: str
    access_token_expiry: datetime
    refresh_token: str

#Ad Account -> Campaigns -> Ad Set -> Ads

# Ad Account Model
class AdAccount(BaseModel):
    organization_id: int = None
    platform: str
    account_id: str
    name: str
    currency: str
    timezone: Optional[str] = None
    spend_cap: Optional[float] = None
    balance: Optional[float] = None
    created_at: datetime = datetime.utcnow()
    campaigns: List["Campaign"] = None    

# Campaign Model
class Campaign(BaseModel):
    id: int
    ad_account_id: int
    campaign_id: str
    name: str
    status: str  # 'Active', 'Paused', 'Archived'
    objective: Optional[str]
    budget_type: str  # 'Daily', 'Lifetime'
    budget_amount: Optional[float]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    created_at: datetime

    def to_json(self) -> Dict[str, Any]:
        return self.dict()

# Ad Set Model
class AdSet(BaseModel):
    id: int
    campaign_id: int
    ad_set_id: str
    name: str
    status: str  # 'Active', 'Paused', 'Archived'
    bid_strategy: Optional[str]  # 'Manual', 'Automated'
    bid_amount: Optional[float]
    audience_targeting: Optional[Dict[str, Any]]  # JSONB
    placement: List[str]  # Array of placements
    schedule: Optional[Dict[str, Any]]  # JSONB
    created_at: datetime

    def to_json(self) -> Dict[str, Any]:
        return self.dict()

# Ad Model
class Ad(BaseModel):
    id: int
    ad_set_id: int
    ad_id: str
    name: str
    status: str  # 'Active', 'Paused', 'Archived'
    format: str  # 'Image', 'Video', 'Carousel', 'Text'
    headline: Optional[str]
    description: Optional[str]
    destination_url: Optional[str]
    cta: Optional[str]
    media_url: Optional[str]
    created_at: datetime


class Audience(BaseModel):
    AUDIENCE: str






class AdPlatform(Enum):
    FB = "FB"
    INSTAGRAM = "INSTAGRAM"
    TIKTOK = "TIKTOK"
    LINKEDIN = "LINKEDIN"
    X = "X"
    REDDIT = "REDDIT"
    GOOGLE_ADS = "GOOGLE_ADS"

class TemplateType(Enum):
    CUSTOM = "CUSTOM"
    
    #awareness
    NEW_LAUNCH = "NEW_LAUNCH"
    SEASONAL_BUZZ = "SEASONAL_BUZZ"
    TRENDS = "TRENDS"

    #engagement
    PROMOTE_ITEM = "PROMOTE_ITEM"
    COMPARISON = "COMPARISON"
    RESOURCE = "RESOURCE"

    #conversion
    FLASH_SALE = "FLASH_SALE"
    FREE_TRIAL = "FREE_TRIAL"
    CART_ABANDON = "CART_ABANDON"
    LIMITED_STOCK = "LIMITED_STOCK" 
    REFERAL = "REFERAL" #refer a friend; get $X 


class Objective(Enum):
    AWARENESS = "AWARENESS"
    ENGAGEMENT = "ENGAGEMENT"
    CONVERSION = "CONVERSION"

class CampaignTemplate(BaseModel):
    campaign_template_id: int
    objective: Objective
    global_budget: int
    global_budget_currency: str
    industry: str
    status: str

class AdTemplate(BaseModel):
    campaign_template_id: int
    ad_template_id: int
    ad_platform: str
    audience: str

# class PromoteItemAd(BaseModel):




