from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from sqlalchemy import Table
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from .controllers import digital_product as digital_product_controller, \
    user as user_controller
from .database import engine, Base, SessionLocal
from .data.models import *
from .data.setup.data_setup_from_csv import DataSetupFromCSV
from .data.setup.basic_data_setup import BasicDataSetup
from .utils import file_model_modifier_mappings


def perform_initial_data_setup(data_setup: BasicDataSetup, tables_to_create: list[Table]):
    with SessionLocal() as session:
        data_setup.create_tables(Base, engine, tables_to_create)
        data_setup.perform_data_insertion_if_required(session)

@asynccontextmanager
async def lifespan(app: FastAPI):
    tables_to_create = [Address.__table__, DigitalProduct.__table__, PhysicalProduct.__table__, Store.__table__, 
                        User.__table__, StoresPhysicalProducts.__table__]
       
    data_setup_csv = DataSetupFromCSV(file_model_modifier_mappings)
    perform_initial_data_setup(data_setup_csv, tables_to_create)
    yield

templates = Jinja2Templates(directory="app/templates")

app = FastAPI(lifespan=lifespan)

app.include_router(digital_product_controller.router)
app.include_router(user_controller.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def root():
    return RedirectResponse(url=digital_product_controller.router.prefix)
 