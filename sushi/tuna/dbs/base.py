from sqlalchemy.orm import Session
from abc import ABC, abstractmethod

class BaseDB(ABC):
    @abstractmethod
    def create_db(self)->Session:
        pass

    @abstractmethod
    def dispose(self):
        pass