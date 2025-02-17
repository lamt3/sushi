import logging
from fastapi import APIRouter, HTTPException
from tuna.dtos.member_dto import MemberDTO
from tuna.services.home_service import HomeService
import requests
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class GoogleAuthTokenRequest(BaseModel):
    token: str


class HomeHandler:
    def __init__(self, hs: HomeService):
        self.hs = hs

    async def health(self):
        return await self.hs.get_home()
    
    async def login_member(self, request: GoogleAuthTokenRequest):
        try:
            if request == None or request.token == None or request.token == "":
                raise HTTPException(status_code=401, detail="Invalid Google Credentials. Please Login with Valid Gmail.")

            return await self.hs.login_member(request.token)
        except Exception as e:
            logger.error(f"Failed HomeHandler.login_member(): {e}")
            raise HTTPException(status_code=401, detail=f"Error Logging In User. Please Contact Support.")
    
    async def create_organization(self):
        return await self.hs.get_home()
    
    async def approve_member_to_organization(self):
        return await self.hs.get_home()
