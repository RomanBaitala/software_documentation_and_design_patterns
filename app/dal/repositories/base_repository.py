from ..interfaces import IBaseRepository
from ...config.ext import db
from typing import TypeVar, Optional, List

T = TypeVar('T')

class BaseRepository(IBaseRepository[T]):
    def __init__(self, model):
        self.model = model

    def get_by_id(self, id: int) -> Optional[T]:
        return self.model.query.get(id)
    
    def get_all(self) -> List[T]:
        return self.model.query.all()
    
    def create(self, entity: T) -> T:
        db.session.add(entity)
        db.session.commit()
        return entity
    
    def update(self, entity: T) -> T:
        db.session.commit()
        return entity
    
    def delete(self, id: int) -> None:
        entity = self.get_by_id(id)
        if entity:
            db.session.delete(entity)
            db.session.commit()