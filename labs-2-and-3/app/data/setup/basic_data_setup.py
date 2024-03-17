from abc import ABC, abstractmethod
from sqlalchemy import Table, Engine
from sqlalchemy.orm import Session

class BasicDataSetup(ABC):
    @abstractmethod
    def _is_default_data_present(self, mapping, session: Session):
        pass
    
    @abstractmethod
    def _delete_data_from_table(self, model_class, session: Session):
        pass
    
    @abstractmethod
    def _insert_data(self, mapping, session: Session):
        pass

    @abstractmethod
    def perform_data_insertion_if_required(self, session: Session):
        pass

    def create_tables(self, base, engine: Engine, tables_to_create: list[Table]):
        base.metadata.create_all(bind=engine, tables=tables_to_create)
