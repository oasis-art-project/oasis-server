# -*- coding: utf-8 -*-

"""
Part of the OASIS project - https://github.com/oasis-local-art
Copyright (c) 2019 DUOpoly
License Artistic-2.0
"""

from marshmallow import validate, fields
from marshmallow_sqlalchemy import ModelSchemaOpts, ModelSchema

from src.backend.extensions import db


class SurrogatePK(object):
    """
    Surrogate Primary Key for inheritance by models. Helps to avoid incorrect ID type
    """
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    tags = db.Column(db.String(100), nullable=True)

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
    def __init__(self, meta, **kwargs):
        if not hasattr(meta, "sql_session"):
            meta.sqla_session = db.session
        super(BaseOpts, self).__init__(meta, **kwargs)


class BaseSchema(ModelSchema):
    OPTIONS_CLASS = BaseOpts
    
    # Overwritten fields
    tags = fields.Str(allow_none=True, validate=validate.Length(max=100))