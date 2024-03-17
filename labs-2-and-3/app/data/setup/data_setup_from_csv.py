import os
import csv
import logging

from sqlalchemy.orm import Session

from app.constants import GENERATED_DATA_DIR
from app.utils import FileModelMapping
from app.data.models import *
from app.data.setup.basic_data_setup import BasicDataSetup


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataSetupFromCSV(BasicDataSetup):
    def __init__(self, file_model_modifier_mappings: list[FileModelMapping]):
        self.file_model_modifier_mappings = file_model_modifier_mappings

    def _is_default_data_present(self, mapping: FileModelMapping, session: Session):
        logger.info(f"Checking if default data is present for {mapping.model_class.__name__}")
        return session.query(mapping.model_class).count() >= mapping.num_rows_generated

    def _delete_data_from_table(self, model_class, session: Session):
        logger.info(f"Deleting data from table {model_class.__name__}")
        session.query(model_class).delete()
        session.commit()
        logger.info(f"Data deletion completed for table {model_class.__name__}")

    def _insert_data(self, mapping: FileModelMapping, session: Session):
        logger.info(f"Inserting data into table {mapping.model_class.__name__}")
        file_path = os.path.join(GENERATED_DATA_DIR, mapping.file_name)
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            foreign_id = 1
            for row in reader:
                if mapping.modifier_function and mapping.model_class == Store:
                    row = mapping.modifier_function(row, foreign_id)
                    foreign_id += 1
                session.add(mapping.model_class(**row))
            session.commit()
        logger.info(f"Data insertion completed for table {mapping.model_class.__name__}")

    def perform_data_insertion_if_required(self, session: Session):
        logger.info("Performing data insertion if required")
        for mapping in self.file_model_modifier_mappings:
            if not self._is_default_data_present(mapping, session):
                logger.info(f"Default data not present for {mapping.model_class.__name__}")
                self._delete_data_from_table(mapping.model_class, session)
                self._insert_data(mapping, session)
            else:
                logger.info(f"Default data present for {mapping.model_class.__name__}")
        logger.info("Data insertion completed")
