from flask_restplus import Resource, reqparse, Api
from models import db, Country
from sqlalchemy.dialects.postgresql import JSONB
from flask import Blueprint
import itertools
import re
import urllib
from operator import itemgetter


def code_from_symbol(input_symbol=None, excluded_currencies={}):
    """
    Provides ISO code from input
    :param input_symbol: Currency symbol to parse - if it is a ISO code or
    in excluded_currencies returns ISO code of this symbol,
    else tries to parse the symbol and lookup ISO code
    :param excluded_currencies: Dictionary of common currencies
    with symbols - i.e USD - $, GBP - £
    :return: Returns ISO code
    """
    try:
        if re.match(r"[A-Z]{3}", input_symbol, re.IGNORECASE) is not None:
            return input_symbol
        elif input_symbol in excluded_currencies.values():
            return [
                key
                for key, value in excluded_currencies.items()
                if value == input_symbol
            ][0]
        elif input_symbol not in excluded_currencies.values():
            currencies = fetch_currencies_by_symbol(input_symbol)

            if len(currencies) == 1:

                return currencies[0]["value"]
            else:

                for index, item in enumerate(all_symbols()):
                    if (
                        item["alt_symbol"] == input_symbol
                        or item["alt_symbol"] == input_symbol.upper()
                    ):

                        return item["code"]
                    elif item["symbol"] == input_symbol:

                        return item["code"]

        elif (
            input_symbol not in excluded_currencies.values()
            and re.match(r"[A-Z]{3}", input_symbol, re.IGNORECASE) is None
        ):
            currencies = fetch_currencies_by_symbol(input_symbol)
            if len(currencies) == 1:
                return currencies[0]["value"]
            else:

                for index, item in enumerate(all_symbols()):
                    if (
                        item["alt_symbol"] == input_symbol
                        or item["alt_symbol"] == input_symbol.upper()
                    ):

                        return item["code"]
                    elif item["symbol"] == input_symbol:
                        return item["code"]

        else:
            return input_symbol
    except Exception:
        raise ValueError(f"Unable to parse {input_symbol}")


def all_symbols():
    """
    Looks up countries table to provide currencies
    :return: Returns dict with all available currencies,
    their symbols, ISO codes,
    names, and alt symbols which are combination of ISO code + symbol
    to distinguish currencies denominated by the same symbol,
    i.e. AU$ = Australian Dollar
    """
    val = db.column("value", type_=JSONB)
    symbols = (
        db.session.query(
            val["symbol"].astext, val["name"].astext, val["code"].astext
        )
        .select_from(
            Country, db.func.jsonb_array_elements(Country.currencies).alias()
        )
        .all(),
    )

    symbols = list(set(itertools.chain.from_iterable(symbols)))
    result = []
    for elem in symbols:
        if (elem[0] is not None and elem[0] != "(none)") and (
            elem[1] is not None and elem[2] is not None
        ):
            el_dict = {
                "symbol": elem[0],
                "name": elem[1],
                "code": elem[2],
                "alt_symbol": elem[2][0:2] + elem[0],
            }
            if el_dict["symbol"] == "Br":
                el_dict["alt_symbol"] = elem[2][0:3] + elem[0]
            result.append(el_dict)
    return result


def unique_by_key(elements, key=None):
    """
    Helper function to provide unique values according to given key
    :param elements: Iterable obj
    :param key: Key to filter
    :return:
    """
    if key is None:
        # no key: the whole element must be unique
        key = lambda e: e
    return {key(el): el for el in elements}.values()


api_bp = Blueprint("api", __name__)
api = Api(api_bp)

parser = reqparse.RequestParser(bundle_errors=True)


def fetch_currencies_by_symbol(symbol):
    """
    Queries table countries to provide a
    dict of currencies associated with given symbol
    :param symbol: Currency symbol for querying db
    :return: Returns dict with all currencies with given symbol
    """
    val = db.column("value", type_=JSONB)
    currencies = (
        db.session.query(val["code"].astext, val["name"].astext)
        .select_from(
            Country, db.func.jsonb_array_elements(Country.currencies).alias()
        )
        .filter(val.contains({"symbol": symbol}))
        .all(),
    )

    currencies = unique_by_key(
        list(set(list(itertools.chain.from_iterable(currencies)))),
        key=itemgetter(0),
    )
    result = []
    for elem in currencies:
        if (elem[0] is not None and elem[0] != "(none)") and (
            elem[1] is not None
        ):
            el_dict = {"value": elem[0], "name": elem[1]}
            result.append(el_dict)
    return result


class SymbolResource(Resource):
    parser.add_argument(
        "symbol", type=str, help="Symbol to find currency codes for"
    )

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
        if args["symbol"]:

            response = fetch_currencies_by_symbol(
                urllib.parse.unquote(args["symbol"])
            )
            if response:
                return ({"status": "success", "symbols": response}, 200, {})

            return (
                {
                    "status": "not_found",
                    "message": "Requested symbol was not found",
                },
                404,
                {},
            )

        return ({"status": "success", "symbols": all_symbols()}, 200, {})
