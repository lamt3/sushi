import datetime

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
