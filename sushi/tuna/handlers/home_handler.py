import json
import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from tuna.auth.jwt import create_jwt_token
from tuna.dtos.member_dto import MemberDTO
from tuna.services.home_service import HomeService
import requests
from pydantic import BaseModel
from fastapi import Response
from fastapi import Cookie

logger = logging.getLogger(__name__)

class GoogleAuthTokenRequest(BaseModel):
    token: str


class HomeHandler:
    def __init__(self, hs: HomeService):
        self.hs = hs

    async def health(self):
        return await self.hs.get_home()
    
    async def verify_auth(self, request: Request):
        return request.state.user
        # return {"status": "ok"}
    
    async def login_member(self, request: GoogleAuthTokenRequest, response:Response):
        try:
            if request == None or request.token == None or request.token == "":
                raise HTTPException(status_code=401, detail="Invalid Google Credentials. Please Login with Valid Gmail.")

            member = await self.hs.login_member(request.token)
            jwt_token = create_jwt_token(member)
            
            response.set_cookie(
                key="token",
                value=jwt_token,
                httponly=True,
                secure=True,
                samesite="none",
                max_age=15767999,
                path="/",
            )
            
            # Set the response body
            response.body = json.dumps(member.to_json()).encode('utf-8')
            response.status_code = 200
            return response
        except Exception as e:
            logger.error(f"Failed HomeHandler.login_member(): {e}")
            raise HTTPException(status_code=401, detail=f"Error Logging In User. Please Contact Support.")
    
    async def create_organization(self):
        return await self.hs.get_home()
    
    async def approve_member_to_organization(self):
        return await self.hs.get_home()
    
    async def get_dashboard(self, request: Request):
        print(request.cookies.get("token"))
        print()
        print(request.state.user)
        return {
            # "campaigns" : [ {
            # "id": 1,
            # "name": 'Summer Sale 2024',
            # "objective": 'Conversions',
            # "platforms": ['facebook', 'instagram', 'linkedin'],
            # "createdBy": 'John Doe',
            # "createdAt": '2024-02-20',
            # "updatedAt": '2024-02-21',
            # "status": 'Active',
            # }],
            # "organization": {
            #     "organization_id":1, 
            #     "name": "my_org"
            # }
            "campaigns":[],
            "organization": {
                "organization_id":1, 
                "name": "my_org"
            }
        }
