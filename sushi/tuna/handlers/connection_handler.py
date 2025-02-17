from tuna.integrations.destinations.connection import AdToken, get_oauth_service
from fastapi.responses import RedirectResponse
from fastapi import HTTPException


class ConnectionHandler:
    # def __init__(self):
        # self.hs = hs

    def get_auth_url(self, ad_platform:str):
        ad_oauth_service = get_oauth_service(ad_platform)
        if ad_oauth_service == None:
            raise HTTPException(status_code=404, detail=f"ad_platform: {ad_platform} not found")
        
        auth_url = ad_oauth_service.get_auth_url()
        return RedirectResponse(auth_url)
    
    async def get_oauth_token(self, ad_platform:str, code: str):
        try: 
            ad_oauth_service = get_oauth_service(ad_platform)
            if ad_oauth_service == None:
                raise HTTPException(status_code=404, detail=f"ad_platform: {ad_platform} not found")
            token_data = await ad_oauth_service.exchange_code_for_token(code)
            return {"message": "OAuth successful", "data": token_data}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
   

