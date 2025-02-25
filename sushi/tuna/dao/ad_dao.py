from tuna.dtos.ad_dto import AdConnectionDTO
from tuna.dtos.member_dto import MemberDTO
from tuna.dbs.base import QueryBuilder
from sqlalchemy import Result, text, Row
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TypeVar, Optional, Callable, Any


class AdDAO:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    
    async def get_access_token(self, organization_id: str, ad_platform: str):
        query = """
        select access_token 
        from ad_platforms 
        where organization_id = :organization_id 
        and ad_platform_name = :ad_platform
        """

        params = {
            "organization_id": organization_id,
            "ad_platform_name": ad_platform
        }

        qb = QueryBuilder()
        access_token = await (qb.session(self.db())
                                .query(query)
                                .params(params)
                                .execute_read(lambda r : self._map_access_token(r)))
        return access_token
    
    def _map_access_token(self, r: Result):
        row = r.mappings().first()
        return row["access_token"]
    
    async def insert_ad_platform(self, organization_id: int, adc: AdConnectionDTO):
        query = """
        INSERT INTO ad_platforms (
        organization_id,
        ad_platform_name,
        access_token,
        access_token_expiry,
        refresh_token
        ) VALUES (
            :organization_id,
            :ad_platform_name,
            :access_token,
            :access_token_expiry,
            :refresh_token
        )
        ON CONFLICT (organization_id, ad_platform_name) 
        DO UPDATE SET
            access_token = EXCLUDED.access_token,
            access_token_expiry = EXCLUDED.access_token_expiry,
            refresh_token = EXCLUDED.refresh_token;
        """

        params = adc.to_json()
        params["organization_id"] = organization_id
        
        session: AsyncSession = self.db()
        query_builder = QueryBuilder()
        await (query_builder
            .session(session)
            .query(query)
            .params(params)
            .execute_write())
    