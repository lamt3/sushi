from tuna.dtos.ad_dto import AdConnectionDTO
from tuna.dtos.member_dto import MemberDTO
from tuna.dbs.base import QueryBuilder
from sqlalchemy import text, Row
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TypeVar, Optional, Callable, Any


class AdDAO:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

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
    