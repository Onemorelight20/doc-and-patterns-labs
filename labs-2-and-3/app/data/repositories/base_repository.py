from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

class BaseRepository(ABC):
    @abstractmethod
    def get_by_id(self, db: Session, id: int):
        pass

    @abstractmethod
    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        pass

    @abstractmethod
    def create(self, db: Session, entity):
        pass

    @abstractmethod
    def update(self, db: Session, id, entity):
        pass

    @abstractmethod
    def delete(self, db: Session, id):
        pass
