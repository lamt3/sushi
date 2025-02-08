
from tuna.dao.company_dao import CompanyDAO


class HomeService:
    def __init__(self, company_dao: CompanyDAO):
        self.company_dao = company_dao

    def get_home(self):
        
        print('hi')