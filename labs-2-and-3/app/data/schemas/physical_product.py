from app.data.schemas.product import ProductBase

class PsysicalProductBase(ProductBase):
    amount_available: int

class DigitalProductCreate(PsysicalProductBase):
    pass

class DigitalProduct(PsysicalProductBase):
    id: int

    class Config:
        from_attributes = True
