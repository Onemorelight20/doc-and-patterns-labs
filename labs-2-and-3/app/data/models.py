from sqlalchemy import Column, Integer, String, Numeric, Table, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship, mapped_column
from app.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password_encoded = Column(String)
    payer_cohort = Column(String)
    first_name = Column(String)
    last_name = Column(String)


class Product(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Numeric(10, 2))


class DigitalProduct(Product):
    __tablename__ = 'digital_products'
    
    encryption_key = Column(String)


class StoresPhysicalProducts(Base):
    __tablename__ = 'stores_physical_products'

    store_id = Column(Integer, ForeignKey('stores.id'), primary_key=True)
    physical_product_id = Column(Integer, ForeignKey('physical_products.id'), primary_key=True)


class PhysicalProduct(Product):
    __tablename__ = 'physical_products'

    weight = Column(Float)
    amount_available = Column(Integer)
    stores = relationship('Store', secondary="stores_physical_products", back_populates='physical_products')


class Store(Base):
    __tablename__ = 'stores'

    id = Column(Integer, primary_key=True)
    lon = Column(Numeric(10, 2))
    lat = Column(Numeric(10, 2))
    workers_amount = Column(Integer)
    is_flagship = Column(Boolean)
    address_id =  mapped_column(ForeignKey('addresses.id'))
    address = relationship('Address', back_populates='store')

    physical_products = relationship('PhysicalProduct', secondary="stores_physical_products", back_populates='stores')


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True, index=True)
    street = Column(String)
    city = Column(String)
    state = Column(String)
    postal_code = Column(Integer)
    country = Column(String)
    store = relationship('Store', back_populates='address')