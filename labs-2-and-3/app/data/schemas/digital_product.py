from fastapi import Form
from app.data.schemas.product import ProductBase



class DigitalProductBase(ProductBase):
    encryption_key: str
    

class DigitalProductCreate(DigitalProductBase):
    pass

class DigitalProduct(DigitalProductBase):
    id: int

    class Config:
        from_attributes = True
