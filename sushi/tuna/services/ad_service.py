from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from tuna.integrations.ads_clients.client import AdClient
from tuna.integrations.destinations.connection import AdOAuthClient
from tuna.dao.ad_dao import AdDAO
from tuna.dtos.ad_dto import AdAccount



class AdService:
    def __init__(self, ad_dao: AdDAO):
        self.ad_dao = ad_dao
    
    def get_auth_url(self, ad_platform:str, callback_url:str)->str:
        oauth_client = AdOAuthClient.get_client(ad_platform)
        if oauth_client == None:
            raise Exception(detail=f"ad_platform: {ad_platform} not found")

        return oauth_client.get_auth_url(callback_url)
        
    async def add_oauth_connection(self, organization_id: int, ad_platform: str, code: str):
        oauth_client = AdOAuthClient.get_client(ad_platform)
        if oauth_client == None:
            raise Exception(detail=f"ad_platform: {ad_platform} not found")
        
        ac_dto = await oauth_client.exchange_code_for_token(code)
        await self.ad_dao.insert_ad_platform(organization_id=organization_id, adc=ac_dto)

    async def get_ad_accounts(self, organization_id: int, ad_platform: str):
        ad_client = AdClient.get_ad_client(ad_platform)
        if ad_client == None:
            raise Exception(detail=f"ad_platform: {ad_platform} not found")
        
        access_token = await self.ad_dao.get_access_token(organization_id, ad_platform)
        if access_token == None or access_token == "":
            raise Exception("No FB Access Token")
        
        return ad_client.get_ad_accounts(access_token)

    async def add_ad_accounts(self, ad_accounts: List[AdAccount]):
        await self.ad_dao.insert_ad_accounts(ad_accounts)
        
        