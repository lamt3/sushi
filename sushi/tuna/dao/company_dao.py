from tuna.dbs.base import BaseDB
from sqlalchemy import text

class CompanyDAO:
    def __init__(self, db: BaseDB) -> None:
        self.db = db.create_db()

    async def get_company(self):
        print('hi')
        try:
            async with self.db() as session:
                return await session.execute(text("SELECT * FROM TEST"))
        except Exception as e:
            print(e)
        
        

