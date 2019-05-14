import pytest
from resources.Symbol import *
from utils.default_symbols import default_symbols


def test_symbol_resource_args(client):
    response = client.get("/api/symbols?symbol=¥")
    assert response.status_code == 200
    assert len(response.json["symbols"]) == 2


def test_symbol_resource(client):
    response = client.get("/api/symbols")
    assert response.status_code == 200
    assert response.json["symbols"][0]["code"] is not None
    assert response.json["symbols"][-1]["code"] is not None
    assert len(response.json["symbols"]) > 1


def test_bad_arg(client):
    response = client.get("/api/symbols?arg=Foo")
    assert response.status_code == 400
    assert response.json == {"message": "Unknown arguments: arg"}


def test_not_found(client):
    response = client.get("/api/symbols?symbol=Foo")
    assert response.status_code == 404
    assert response.json == {
        "status": "not_found",
        "message": "Requested symbol was not found",
    }


def test_code_from_symbol_returns_ISO():
    result = code_from_symbol("EUR", excluded_currencies=default_symbols)
    assert result == "EUR"


def test_code_from_symbol_from_excluded():
    result = code_from_symbol("$", excluded_currencies=default_symbols)
    assert result == "USD"


def test_code_from_symbol_is_unique(client):
    result = code_from_symbol("Kč", excluded_currencies=default_symbols)
    assert result == "CZK"


def test_code_from_symbol_is_first_applicable(client):
    result = code_from_symbol("Sh", excluded_currencies=default_symbols)
    assert result is not None


def test_code_from_symbol_invalid(client):
    assert (
        code_from_symbol("Kčasfasgsa", excluded_currencies=default_symbols)
    ) is None

