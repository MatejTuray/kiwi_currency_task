from flask import Blueprint
from flask_restplus import Api
from resources.Countries import CountriesResource
from resources.Symbol import SymbolResource
from resources.Convert import ConvertResource


api_bp = Blueprint("api", __name__)
api = Api(api_bp, default_label="Currency converter API", doc="/docs")


api.add_resource(CountriesResource, "/countries")
api.add_resource(ConvertResource, "/currency_converter")
api.add_resource(SymbolResource, "/symbols")
