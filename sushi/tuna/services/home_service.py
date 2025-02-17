
import logging
from tuna.dao.member_dao import MemberDAO
from tuna.dtos.member_dto import MemberDTO
import requests

logger = logging.getLogger(__name__)

class HomeService:
    def __init__(self, member_dao: MemberDAO):
        self.mdao = member_dao
        
    async def get_home(self):
        return await self.mdao.test()
    
    async def login_member(self, google_access_token:str):
        resp = requests.get(
                url = "https://www.googleapis.com/oauth2/v3/userinfo", 
                headers={"Authorization": f"Bearer {google_access_token}"}
            )
        
        if resp.status_code != 200:
            logger.error(f"Failed HomeHandler.login_member() Google API Auth Failed. Status Code:{resp.status_code} Error: {resp.json()}")
            raise Exception("Invalid Google Credentials. Please Login with Valid Gmail.")
        
        google_user = resp.json()
        member = MemberDTO.from_google_user(google_user)
        return await self.mdao.insert_member(member)
        