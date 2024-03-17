from collections import namedtuple
from app.data.models import *
from app.constants import *

def modify_store_entity_row(row: dict[str, str], address_id) -> dict[str, str]:
    row['is_flagship'] = True if row['is_flagship'] == 'True' else False
    row['address_id'] = address_id
    return row

FileModelMapping = namedtuple('FileModelMapping', ['file_name', 'model_class', 'modifier_function', 'num_rows_generated'])


file_model_modifier_mappings = [
    FileModelMapping(USER_DATA_FILE_NAME, User, None, USER_DATA_ROWS_NUMBER),
    FileModelMapping(DIGITAL_PRODUCT_DATA_FILE_NAME, DigitalProduct, None, DIGITAL_PRODUCT_DATA_ROWS_NUMBER),
    FileModelMapping(PHYSICAL_PRODUCT_DATA_FILE_NAME, PhysicalProduct, None, PHYSICAL_PRODUCT_DATA_ROWS_NUMBER),
    FileModelMapping(STORE_DATA_FILE_NAME, Store, modify_store_entity_row, STORE_DATA_ROWS_NUMBER),
    FileModelMapping(ADDRESS_DATA_FILE_NAME, Address, None, ADDRESS_DATA_ROWS_NUMBER),
    FileModelMapping(STORES_PHYSICAL_PRODUCTS_DATA_FILE_NAME, StoresPhysicalProducts, None, STORES_PHYSICAL_PRODUCTS_DATA_ROWS_NUMBER)
]
