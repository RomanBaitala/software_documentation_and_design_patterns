from ..interfaces import IBaseRepository
from ...config.ext import db
from typing import TypeVar, Optional, List
from sqlalchemy.exc import SQLAlchemyError
import logging

T = TypeVar('T')

class BaseRepository(IBaseRepository[T]):
    def __init__(self, model):
        self.model = model

    def get_by_id(self, id: int) -> Optional[T]:
        try:
            return self.model.query.get(id)
        except SQLAlchemyError as e:
            logging.error(f"Error fetching {self.model.__name__} by id {id}: {e}")
            return None
    
    def get_all(self) -> List[T]:
        try:
            return self.model.query.all()
        except SQLAlchemyError as e:
            logging.error(f"Error fetching all {self.model.__name__}: {e}")
            return []
    
    def create(self, entity: T) -> T:
        try:
            db.session.add(entity)
            db.session.commit()
            return entity
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"Error creating {self.model.__name__}: {e}")
            raise e 
    
    def update(self, entity: T) -> T:
        try:
            db.session.commit()
            return entity
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"Error updating {self.model.__name__}: {e}")
            raise e
    
    def delete(self, id: int) -> bool:
        try:
            entity = self.get_by_id(id)
            if entity:
                db.session.delete(entity)
                db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error(f"Error deleting {self.model.__name__} with id {id}: {e}")
            raise e