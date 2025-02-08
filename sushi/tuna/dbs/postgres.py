
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from abc import ABC, abstractmethod

from tuna.dbs.base import BaseDB

class Config(ABC):
    POSTGRES_USERNAME = "postgres"
    POSTGRES_DB_NAME = "postgres"
    # localhost for development purposes
    POSTGRES_HOST = "localhost"
    POSTGRES_PORT = "5432"
    # password stored in .env file
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    SQL_COMMAND_ECHO = False


class PostgresDB(BaseDB):
    def __init__(self) -> None:
        super().__init__()
        self._async_engine = create_async_engine(
            self._get_connection_string(),
            echo=Config.SQL_COMMAND_ECHO,
            pool_size=15,        # Optimal pool size based on your tests
            max_overflow=5,      # Temporary connections beyond pool_size
            pool_timeout=30,     # Timeout for connection wait
            pool_recycle=1800    # Recycle connections to avoid stale ones
        )

    def _get_connection_string(driver: str = "asyncpg") -> str:
        return f"postgresql+{driver}://{Config.POSTGRES_USERNAME}:{Config.POSTGRES_PASSWORD}@{Config.POSTGRES_HOST}:{Config.POSTGRES_PORT}/{Config.POSTGRES_DB_NAME}"

    def create_db(self)->Session:
        return sessionmaker(self._async_engine, class_=AsyncSession)
    
    def dispose(self):
        return self._async_engine.dispose()
        
