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
import sqlalchemy
from sqlalchemy import text

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
       
        connection_params = {
            "username": self.user,
            "password": self.password,
            "port": self.port,
            "database": self.database,
            "drivername": "postgresql+asyncpg",
            "host": self.host
        }
        logger.info(f"Creating DB Engine with params: {connection_params}")

        url = sqlalchemy.engine.url.URL.create(**connection_params)
        self._async_engine = create_async_engine(
            url,
            echo=Config.SQL_COMMAND_ECHO,
            pool_size=15,
            max_overflow=5,
            pool_timeout=30,
            pool_recycle=1800
        )

    def create_db(self)->Session:
        return sessionmaker(self._async_engine, class_=AsyncSession)
    
    async def dispose(self):
        return await self._async_engine.dispose()
        
    async def test_connection(self):
        try:                
            async with self._async_engine.connect() as c:
                await c.execute(text('SELECT * FROM TEST'))
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            raise
           

