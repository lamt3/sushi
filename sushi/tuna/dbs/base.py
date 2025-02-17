from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC, abstractmethod

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