from flask_restplus import Resource, reqparse, Api
from run import redis
from slugify import slugify
from utils.Convertor import Convertor
from resources.Symbol import code_from_symbol
import json
from utils.default_symbols import default_symbols
from flask import Blueprint
import urllib

api_bp = Blueprint("api", __name__)
api = Api(api_bp)
parser = reqparse.RequestParser(bundle_errors=True)
cnv = Convertor()


def fetch_and_calculate_single(args):
    """
    :param args: Args parsed by the Convert resource class,
    input and output currencies in ISO code
    :return: Returns dict with output.
    If the exchange rate of given currency pair is in cache,retrieves it,
    else passes args to Convertor
    class to retrieve it and calculate the output, caches the rate
    """
    rate = redis.get(
        slugify(f'{args["input_currency"]}:{args["output_currency"]}')
    )
    if rate is None:
        try:
            exchange = cnv.get_single_rate(
                args["input_currency"], args["output_currency"]
            )
            redis.setex(
                name=slugify(
                    f'{args["input_currency"]}:{args["output_currency"]}'
                ),
                time=60 * 60,
                value=exchange,
            )
            result = cnv.calculate(
                args["amount"],
                args["input_currency"],
                args["output_currency"],
                float(exchange),
            )
            return result
        except Exception:
            raise ValueError(
                f"Unable to convert from {args['input_currency']} "
                f"to {args['output_currency']}"
            )

    try:
        result = cnv.calculate(
            args["amount"],
            args["input_currency"],
            args["output_currency"],
            float(rate),
        )
        return result
    except Exception as e:
        raise ValueError(e)


def fetch_calculate_all(args):
    """
    :param args: Args parsed by the ConvertResource class,
     input currency in ISO code
    :return:
    Returns dict with output
    If the exchange rates of EUR - all currencies is in cache,
    retrieves them, else passes args to Convertor
    class to retrieve them, caches the rates, Convertor class
    then calculates the output
    """
    rates = redis.get(slugify(f"all_rates"))
    if rates is None:
        try:
            exchange_rates = cnv.get_all_rates()
            redis.setex(
                name=slugify(f"all_rates"),
                time=60 * 60,
                value=json.dumps(exchange_rates, ensure_ascii=False),
            )
            result = cnv.calculate_all(
                args["amount"], args["input_currency"], exchange_rates
            )
            return result
        except Exception:
            raise ValueError(
                f"Unable to calculate output for ${args['input_currency']}"
            )

    result = cnv.calculate_all(
        args["amount"], args["input_currency"], json.loads(rates)
    )
    return result


class ConvertResource(Resource):
    parser.add_argument(
        "amount", type=float, required=True, help="Amount to convert"
    )
    parser.add_argument(
        "input_currency", type=str, required=True, help="Base currency"
    )
    parser.add_argument("output_currency", type=str, help="Output currency")

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
        try:
            args["input_currency"] = code_from_symbol(
                urllib.parse.unquote(args["input_currency"]),
                excluded_currencies=default_symbols,
            )
            if args["output_currency"]:

                args["output_currency"] = code_from_symbol(
                    urllib.parse.unquote(args["output_currency"]),
                    excluded_currencies=default_symbols,
                )
                data = fetch_and_calculate_single(args)
                if data is None:
                    return (
                        {
                            "status": "not_found",
                            "message": "Unable to find exchange rates",
                        },
                        404,
                        {},
                    )

                return {"status": "success", "data": data}, 200, {}

            data = fetch_calculate_all(args)
            return {"status": "success", "data": data}, 200, {}
        except ValueError as e:
            return {"status": "bad_request", "message": str(e)}, 400, {}
