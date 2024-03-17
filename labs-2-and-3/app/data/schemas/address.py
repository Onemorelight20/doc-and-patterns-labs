from pydantic import BaseModel


class AddressBase(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str
    country: str
