
import logging
from tuna.dtos.shopify_dao import ShopifyDAO
from tuna.dao.member_dao import MemberDAO
from tuna.dtos.member_dto import MemberDTO
import requests

logger = logging.getLogger(__name__)

class HomeService:
    def __init__(self, member_dao: MemberDAO, shopify_dao: ShopifyDAO):
        self.mdao = member_dao
        self.sdao = shopify_dao
        
    async def test(self):
        return await self.mdao.test()
    
    async def login_member(self, google_access_token:str)->MemberDTO:
        resp = requests.get(
                url = "https://www.googleapis.com/oauth2/v3/userinfo", 
                headers={"Authorization": f"Bearer {google_access_token}"}
            )
        
        if resp.status_code != 200:
            logger.error(f"Failed HomeHandler.login_member() Google API Auth Failed. Status Code:{resp.status_code} Error: {resp.json()}")
            raise Exception("Invalid Google Credentials. Please Login with Valid Gmail.")
        
        google_user = resp.json()
        member = MemberDTO.from_google_user(google_user)
        m = await self.mdao.insert_member(member)
        member.member_id = m["member_id"]
        member.organization_id = m["organization_id"]
        member.organization_name = m["organization_name"]
        return member
    
    async def create_organization(self, google_access_token:str)->MemberDTO:
       self.mdao.insert_organization("")
    
    async def connect_shopify_store(self, organization_id, shopify_store):
        await self.sdao.connect_shopify_store(organization_id, shopify_store)

    async def create_shopify_store(self, shopify_store, access_token):
        await self.sdao.insert_shopify_store(shopify_store, access_token)
        