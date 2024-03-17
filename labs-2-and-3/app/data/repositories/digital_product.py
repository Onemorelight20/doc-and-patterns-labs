from sqlalchemy.orm import Session

from app.data.models import DigitalProduct
from app.data.schemas.digital_product import DigitalProductCreate
from .base_repository import BaseRepository


class DigitalProductRepository(BaseRepository):
    @staticmethod
    def get_by_id(db: Session, id: int):
        return db.query(DigitalProduct).filter(DigitalProduct.id == id).first()

    @staticmethod
    def get_by_name(db: Session, name: str):
        return db.query(DigitalProduct).filter(DigitalProduct.name == name).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(DigitalProduct).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, entity: DigitalProductCreate):
        db_product = DigitalProduct(name=entity.name, description=entity.description, price=entity.price, 
                                    encryption_key=entity.encryption_key)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    
    @staticmethod
    def update(db: Session, id: int, entity: DigitalProductCreate):
        db_product = db.query(DigitalProduct).filter(DigitalProduct.id == id).first()
        db_product.name = entity.name
        db_product.description = entity.description
        db_product.price = entity.price
        db_product.encryption_key = entity.encryption_key
        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod
    def delete(db: Session, id: int):
        db_product = db.query(DigitalProduct).filter(DigitalProduct.id == id).first()
        db.delete(db_product)
        db.commit()
        return db_product

    @staticmethod
    def get_total(db: Session):
        return db.query(DigitalProduct).count()
