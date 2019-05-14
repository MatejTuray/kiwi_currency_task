from flask_restplus import Resource, reqparse, Api
from models import Country, CountrySchema
from flask import Blueprint

api_bp = Blueprint("api", __name__)
api = Api(api_bp)
countries_schema = CountrySchema(many=True)
country_schema = CountrySchema()

parser = reqparse.RequestParser(bundle_errors=True)


class CountriesResource(Resource):
    parser.add_argument("name", type=str, help="Country name")

    @api.expect(parser)
    @api.doc(
        responses={
            200: "Sucess - resource found",
            400: "Bad Request - probably invalid query params",
            404: "Not Found - resource not found",
            500: "Internal Server Error - sorry about that one",
        }
    )
    def get(self):
        args = parser.parse_args(strict=True)

        if args["name"]:
            countries = Country.query.filter(
                Country.name.ilike(f"%{args['name']}%")
            ).all()
            countries = countries_schema.dump(countries).data
            if countries:
                return {"status": "success", "data": countries}, 200, {}

            return (
                {"status": "not_found", "message": "Country not found"},
                404,
                {},
            )

        countries = Country.query.all()
        countries = countries_schema.dump(countries).data
        return {"status": "success", "data": countries}, 200, {}
