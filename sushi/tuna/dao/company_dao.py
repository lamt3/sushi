from sushi.tuna.dbs.base import BaseDB

class CompanyDAO:
    def __init__(self, db: BaseDB) -> None:
        self.db = db.create_db()

    def get_company(self):
        print('hi')