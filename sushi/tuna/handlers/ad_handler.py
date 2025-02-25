import json
import logging
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from tuna.services.ad_service import AdService
from tuna.auth.jwt import create_jwt_token
from tuna.dtos.member_dto import MemberDTO
from tuna.dtos.ad_dto import AdAccount
from tuna.services.home_service import HomeService
import requests
from pydantic import BaseModel
from fastapi import Response

logger = logging.getLogger(__name__)

class AdAccountRequest(BaseModel):
    ad_accounts: List[AdAccount]

class AdHandler:
    def __init__(self, ads: AdService):
        self.ads = ads

    async def get_ad_accounts(self, request: Request, ad_platform: str):
        try:
            member: MemberDTO = request.state.member
            return await self.ads.get_ad_accounts(member["organization_id"], ad_platform)
        except Exception as e:
            logging.error(f"AdHandler.get_ad_accounts() error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        
    async def add_ad_accounts(self, request: Request, ar: AdAccountRequest):
        try:
            member: MemberDTO = request.state.member
            for a in ar.ad_accounts: 
                a.organization_id = member["organization_id"]
            await self.ads.add_ad_accounts(ar.ad_accounts)
            return {"status": "success"}
        except Exception as e:
            logging.error(f"AdHandler.get_ad_accounts() error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))