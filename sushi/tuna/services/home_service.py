
from tuna.dbs.base import BaseDB
from tuna.dao.company_dao import CompanyDAO


class HomeService:
    def __init__(self, company_dao: CompanyDAO):
        self.company_dao = company_dao
        

    async def get_home(self):
        return await self.company_dao.get_company()
        