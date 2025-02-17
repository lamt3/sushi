from tuna.dtos.member_dto import MemberDTO
from tuna.dbs.base import BaseDB
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

class MemberDAO:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def test(self):
        try:
            async with self.db() as session:
                return await session.execute(text("SELECT * FROM TEST"))
        except Exception as e:
            print(e)

    async def insert_member(self, member:MemberDTO)->int:

        query = """
         WITH inserted_member AS (
            INSERT INTO members (first_name, last_name, email, member_type)
            VALUES (:first_name, :last_name, :email, :member_type)
            ON CONFLICT (email) DO NOTHING
            RETURNING member_id
        )
        SELECT member_id FROM inserted_member
        UNION
        SELECT member_id FROM members WHERE email = :email;
        """
        
        params = {
            "first_name": member.first_name,
            "last_name": member.last_name,
            "email":  member.email,
            "member_type": member.member_type
        }
        
        try:
            session: AsyncSession = self.db()
            async with session as s:
                async with s.begin():
                    result = await session.execute(text(query), params)
                    row = result.mappings().first()
                    if row is None:
                        raise Exception("Failed to insert or find member")
                    
                    await s.commit()  
                    return row["member_id"]
        except Exception as e:
            await session.rollback() 
            raise Exception(f"Failed to insert or find member: {str(e)} ")
        finally:
            await session.close()
        
        
        

