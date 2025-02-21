from tuna.services.ad_service import AdService
from tuna.integrations.destinations.connection import AdOAuthClient
from fastapi.responses import RedirectResponse
from fastapi import HTTPException
from fastapi import Request
import logging

logger = logging.getLogger(__name__)

class ConnectionHandler:
    def __init__(self, ads: AdService):
        self.ads = ads

    def get_auth_url(self, ad_platform:str, callback_url:str):
        try:
            auth_url = self.ads.get_auth_url(ad_platform, callback_url)
            return RedirectResponse(auth_url)
        except Exception as e:
            logger.error(f"error...{str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
    
    async def get_oauth_token(self, request: Request, ad_platform:str, code: str, state: str):
        try:             
            member = request.state.user
            await self.ads.add_oauth_connection(organization_id=member["organization_id"], ad_platform=ad_platform, code=code)
            return RedirectResponse(url=state)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
   

