# -*- coding: utf-8 -*-

"""
Part of the OASIS ART PROJECT - https://github.com/orgs/oasis-art-project
Copyright (c) 2019-22 TEAM OASIS
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
    files = db.Column(db.String(1000), nullable=True)
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
    files = fields.Str(allow_none=True, validate=validate.Length(max=1000))
    tags = fields.Str(allow_none=True, validate=validate.Length(max=100))