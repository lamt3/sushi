from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class AdConnectionDTO:
    ad_platform_name: str
    access_token: str
    access_token_expiry: datetime
    refresh_token: str

    def __init__(self, ad_platform_name: str, access_token: str, access_token_expiry: datetime, refresh_token: str):
        self.ad_platform_name = ad_platform_name
        self.access_token = access_token
        self.access_token_expiry = access_token_expiry
        self.refresh_token = refresh_token

    def to_json(self):
        return {
            "access_token": self.access_token, 
            "access_token_expiry": self.access_token_expiry,
            "refresh_token": self.refresh_token,
            "ad_platform_name": self.ad_platform_name
        }


# Ad Account Model
class AdAccount(BaseModel):
    id: int
    platform: str
    account_id: str
    name: str
    currency: str
    timezone: Optional[str]
    spend_cap: Optional[float]
    created_at: datetime
    campaigns: List["Campaign"]


    

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

    def to_json(self) -> Dict[str, Any]:
        return self.dict()
