from tuna.integrations.destinations.connection import AdOAuthClient
from tuna.dao.ad_dao import AdDAO

class AdService:
    def __init__(self, ad_dao: AdDAO):
        self.ad_dao = ad_dao
    
    def get_auth_url(self, ad_platform:str, callback_url:str)->str:
        client: AdOAuthClient = AdOAuthClient.get_client(ad_platform)
        if client == None:
            raise Exception(detail=f"ad_platform: {ad_platform} not found")

        return client.get_auth_url(callback_url)
        
    async def add_oauth_connection(self, organization_id: int, ad_platform: str, code: str):
        client: AdOAuthClient = AdOAuthClient.get_client(ad_platform)
        if client == None:
            raise Exception(detail=f"ad_platform: {ad_platform} not found")
        
        ac_dto = await client.exchange_code_for_token(code)
        await self.ad_dao.insert_ad_platform(organization_id=organization_id, adc=ac_dto)