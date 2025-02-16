from tuna.dbs.base import BaseDB
from sqlalchemy import text
from sqlalchemy.orm import Session

class CompanyDAO:
    def __init__(self, db: Session) -> None:
        self.db = db

    async def get_company(self):
        try:
            async with self.db() as session:
                return await session.execute(text("SELECT * FROM TEST"))
        except Exception as e:
            print('error in CompanyDAO get_company()...')
            print(e)
        
        

