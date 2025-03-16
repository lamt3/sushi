from tuna.dbs.base import QueryBuilder
from sqlalchemy import Result, text, Row
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TypeVar, Optional, Callable, Any, List

class ShopifyDAO:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
    
    async def insert_shopify_store(self, shopify_store, access_token):
        query = """
        INSERT INTO shopify_connections (shopify_store, access_token)
        VALUES (:shopify_store, :access_token)
        ON CONFLICT (shopify_store) DO NOTHING;
        """

        params = {
            "shopify_store": shopify_store,
            "access_token": access_token
        }
        session: AsyncSession = self.db()
        qb = QueryBuilder()
        await (
            qb.session(session)
                .query(query)
                .params(params)
                .execute_write()
        )

    async def connect_shopify_store(self, organization_id, shopify_store):
        query = """
        UPDATE shopify_connections
        SET organization_id = :organization_id, updated_at = NOW()
        WHERE shopify_store = :shopify_store;
        """
        params = {
            "organization_id": organization_id,
            "shopify_store": shopify_store
        }
        session: AsyncSession = self.db()
        qb = QueryBuilder()
        await (
            qb.session(session)
                .query(query)
                .params(params)
                .execute_write()
        )

    async def get_shopify_access_token(self, organization_id):
        query = """
        select * 
        FROM shopify_connections
        WHERE organization_id = :organization_id
        """
        params = {
            "organization_id": organization_id,
        }
        session: AsyncSession = self.db()
        qb = QueryBuilder()
        return await (
            qb.session(session)
                .query(query)
                .params(params)
                .execute_read(lambda r: self._map(r))
        )
    
    def _map(self, r: Result):
        row = r.mappings().first()
        print('here in row')
        print(row)
        return {
            "access_token": row["access_token"],
            "shopify_store": row["shopify_store"]
        }