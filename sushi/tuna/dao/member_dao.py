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

    async def insert_member(self, member:MemberDTO):
        query = """
        WITH inserted_member AS (
            INSERT INTO members (first_name, last_name, email, member_type)
            VALUES (:first_name, :last_name, :email, :member_type)
            ON CONFLICT (email) DO NOTHING
            RETURNING member_id, organization_id
        )
        SELECT 
            im.member_id,
            o.organization_id,
            o.name AS organization_name,
            o.created_at AS organization_created_at,
            o.updated_at AS organization_updated_at
        FROM 
            inserted_member im
        LEFT JOIN 
            organizations o ON im.organization_id = o.organization_id
        UNION
        SELECT 
            m.member_id,
            o.organization_id,
            o.name AS organization_name,
            o.created_at AS organization_created_at,
            o.updated_at AS organization_updated_at
        FROM 
            members m
        LEFT JOIN 
            organizations o ON m.organization_id = o.organization_id
        WHERE 
            m.email = :email;
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
                    return {
                        "member_id": row["member_id"],
                        "organization_id": row["organization_id"],
                        "organization_name": row["organization_name"]
                    }  
        except Exception as e:
            raise Exception(f"Failed to insert or find member: {str(e)} ")
        

    async def insert_organization(self, org_name:str)->int:

        query = """
        INSERT INTO organizations (name)
        VALUES (:name)
        ON CONFLICT (name) DO NOTHING
        """
        
        params = {
            "name": org_name
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
        
        
        

