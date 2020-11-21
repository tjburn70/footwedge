from typing import List, Type, TypeVar

from api.database import db_session, Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository:

    def __init__(self, model: Type[ModelType]):
        self.model = model
        self.db_session = db_session

    def get(self, model_id):
        return self.db_session.query(self.model).filter(self.model.id == model_id).first()

    def get_all(self):
        return self.db_session.query(self.model).all()

    def get_by_ids(self, ids: List[int]):
        return self.db_session.query(self.model).filter(self.model.id.in_(ids)).all()

    def create(self, data: dict):
        model_obj = self.model(**data)
        self.db_session.add(model_obj)
        self.db_session.commit()
        self.db_session.refresh(model_obj)
        return model_obj

    def bulk_create(self, records: List[dict]):
        model_objs = [self.model(**record) for record in records]
        self.db_session.add_all(model_objs)
        self.db_session.commit()
        return model_objs

    def update(self, data: dict):
        model_obj = self.model(**data)
        self.db_session.merge(model_obj)
        self.db_session.commit()
        self.db_session.refresh(model_obj)
        return model_obj

    def delete(self, model_id) -> bool:
        is_deleted = self.db_session.query(self.model).filter(self.model.id == model_id).delete()
        self.db_session.commit()
        return is_deleted
