import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from abc import ABC, abstractmethod
import asyncpg
import logging
from tuna.config import Config

from tuna.dbs.base import BaseDB

logger = logging.getLogger(__name__)

class PostgresDB(BaseDB):
    def __init__(self) -> None:
        super().__init__()
        self.host = Config.POSTGRES_HOST
        self.port = Config.POSTGRES_PORT
        self.user = Config.POSTGRES_USERNAME
        self.password = Config.POSTGRES_PASSWORD
        self.database = Config.POSTGRES_DB_NAME
        self.pool = None
        
        # Keep SQLAlchemy engine for other operations
        self._async_engine = create_async_engine(
            self._get_connection_string(),
            echo=Config.SQL_COMMAND_ECHO,
            pool_size=15,
            max_overflow=5,
            pool_timeout=30,
            pool_recycle=1800
        )

    def _get_connection_string(self, driver: str = "asyncpg") -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    def create_db(self)->Session:
        return sessionmaker(self._async_engine, class_=AsyncSession)
    
    async def dispose(self):
        return await self._async_engine.dispose()
        
    async def initialize(self):
        """Call this method when starting your application"""
        await self.init_pool()

    async def test_connection(self):
        if not self.pool:
            await self.init_pool()
        try:
            async with self.pool.acquire() as conn:
                await conn.execute('SELECT 1')
                logger.info("db started successfully")
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            raise
            
    async def init_pool(self):
        try:
            self.pool = await asyncpg.create_pool(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                command_timeout=5,
                timeout=5
            )
        except Exception as e:
            logger.error(f"Failed to initialize database pool: {e}")
            raise
        
