"""
Boston University. Spring 2019
@author: Maxim Tsybanov (oasis@tsybanov.com)
"""

from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchemaOpts, ModelSchema

from src.backend.extensions import db


class SurrogatePK(object):
    """
    Surrogate Primary Key for inheritance by models. Helps to avoid incorrect ID type
    """
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        if any(
            (isinstance(record_id, str) and record_id.isdigit(),
             isinstance(record_id, (int, float))),
        ):
            return cls.query.get(int(record_id))
        return None


class BaseOpts(ModelSchemaOpts):
    """
    Base classes that help to automatically load schemas from models
    class Meta in schema has to use BaseSchema class
    """
    def __init__(self, meta):
        if not hasattr(meta, "sql_session"):
            meta.sqla_session = db.session
        super(BaseOpts, self).__init__(meta)


class BaseSchema(ModelSchema):
    OPTIONS_CLASS = BaseOpts
