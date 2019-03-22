import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()

class BaseMixin(object):

    id = db.Column(UUID(as_uuid=True), default=lambda: uuid.uuid4(), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    modified_at= db.Column(db.DateTime, default=datetime.now())

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
