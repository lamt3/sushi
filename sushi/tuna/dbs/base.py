from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC, abstractmethod

import logging
import sqlalchemy
from sqlalchemy import text, Result
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from tuna.config import Config
from typing import TypeVar, Optional, Callable, Any


logger = logging.getLogger(__name__)

class BaseDB(ABC):
    @abstractmethod
    def create_db(self)->AsyncSession:
        pass

    @abstractmethod
    async def test_connection(self):
        pass
    
    @abstractmethod
    async def dispose(self):
        pass

    # @staticmethod
    
def get_db(db_name:str)->BaseDB:
    if db_name == "postgres":
        return PostgresDB()

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

    def create_db(self)->AsyncSession:
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


T = TypeVar('T')

class QueryBuilder: 
    def __init__(self):
        self._query: Optional[str] = None
        self._params: dict = {}
        self._session: Optional[AsyncSession] = None
        
    def session(self, session: AsyncSession) -> "QueryBuilder":
        """Sets the database session."""
        self._session = session
        return self

    def query(self, query: str) -> "QueryBuilder":
        """Sets the SQL query."""
        self._query = query
        return self

    def params(self, params) -> "QueryBuilder":
        """Sets the query parameters."""
        self._params = params
        return self
    
    async def execute_write(self)->bool:
        try:
            async with self._session as s:
                await s.execute(text(self._query), self._params)
                await s.commit()
        except Exception as e:
            logger.error(f"Failed Write Query: {self._query} With Error: {str(e)}")
            raise Exception(f"Failed Write Query: {str(e)} ")

    async def execute_read(self, result_mapper: Callable[[Result], T])->Optional[T]:
        try:
            session: AsyncSession = self._session
            async with session as s:
                result = await s.execute(text(self._query), self._params)
                return result_mapper(result)
        except Exception as e:
            logger.error(f"Failed Execute Query: {self._query} With Error: {str(e)}")            
            raise Exception(f"Failed to Execute Query: {str(e)} ")