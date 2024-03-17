from sqlalchemy.orm import Session

from app.data.schemas.user import UserCreate
from app.data.models import User
from .base_repository import BaseRepository


class UserRepository(BaseRepository):
    @staticmethod
    def get_by_id(db: Session, id: int):
        return db.query(User).filter(User.id == id).first()

    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, entity: UserCreate):
        fake_hashed_password = entity.password + "notreallyhashed"
        db_user = User(**entity.model_dump(exclude={"password"}), password_encoded=fake_hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
