from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON, JSONB, UUID
from uuid import uuid4

ma = Marshmallow()
db = SQLAlchemy()


class Country(db.Model):
    __tablename__ = "countries"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String(128), nullable=False, unique=True, default=None)
    alpha3Code = db.Column(
        db.String(128), nullable=False, unique=True, default="No alpha3code"
    )
    capital = db.Column(db.String(128), nullable=False, default="No capital")
    currencies = db.Column(JSONB)

    def __repr__(self):
        return f"Country: {self.name}, Alpha3: {self.alpha3Code}"

    def __init__(self, name, alpha3Code, capital, currencies):

        self.name = name
        self.alpha3Code = alpha3Code
        self.capital = capital
        self.currencies = currencies


class CountrySchema(ma.Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True)
    alpha3Code = fields.String(required=True)
    capital = fields.String(required=True)
    currencies = fields.Dict(required=True)


class CurrencySchema(ma.Schema):
    currencies = fields.Dict(required=True)
