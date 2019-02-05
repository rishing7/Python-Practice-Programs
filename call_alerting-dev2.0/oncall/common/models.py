from sqlalchemy.sql import func
from app import db


class BaseModel(db.Model):
    """
    Base Model Class for common model fields across the system

    Create Method: entry **kwargs fields in table
    Bulk Method: Entry of multiple rows in table
    """
    __abstract__ = True

    id = db.Column(db.INTEGER, primary_key=True)
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=func.now())
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now())

    @classmethod
    def create(cls, **kwargs):
        obj = cls(**kwargs)
        db.session.add(obj)
        db.session.commit()

    @classmethod
    def bulk_create(cls, data):
        if isinstance(data, list):
            for row in data:
                obj = cls(**row)
                db.session.add(obj)
            db.session.commit()
        else:
            raise ValueError("Not valid data for bulk operation")
