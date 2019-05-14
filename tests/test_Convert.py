import pytest
from resources.Convert import *


def test_convert(client):
    response = client.get(
        "/api/currency_converter?"
        "amount=10&input_currency=EUR&output_currency=USD"
    )
    assert response.status_code == 200
    assert response.json["data"]["input"]["amount"] == 10
    assert response.json["data"]["input"]["currency"] == "EUR"
    assert response.json["data"]["output"]["USD"] is not None
    assert len(response.json["data"]["output"]) == 1


def test_convert_all(client):
    response = client.get(
        "/api/currency_converter?amount=10&input_currency=EUR"
    )
    assert response.status_code == 200
    assert response.json["data"]["input"]["amount"] == 10
    assert response.json["data"]["input"]["currency"] == "EUR"
    assert response.json["data"]["output"] is not None
    assert len(response.json["data"]["output"]) > 20


def test_convert_unique_symbol(client):
    response = client.get(
        "/api/currency_converter?"
        "amount=10&input_currency=Kč&output_currency=USD"
    )
    assert response.status_code == 200
    assert response.json["data"]["input"]["amount"] == 10
    assert response.json["data"]["input"]["currency"] == "CZK"
    assert response.json["data"]["output"]["USD"] is not None
    assert len(response.json["data"]["output"]) == 1


def test_convert_non_unique_excluded(client):
    response = client.get(
        "/api/currency_converter?"
        "amount=10&input_currency=$&output_currency=Kč"
    )
    assert response.status_code == 200
    assert response.json["data"]["input"]["amount"] == 10
    assert response.json["data"]["input"]["currency"] == "USD"
    assert response.json["data"]["output"]["CZK"] is not None
    assert len(response.json["data"]["output"]) == 1


def test_convert_non_unique_not_excluded(client):
    response = client.get(
        "/api/currency_converter?"
        "amount=10&input_currency=au$&output_currency=Kč"
    )
    assert response.status_code == 200
    assert response.json["data"]["input"]["amount"] == 10
    assert response.json["data"]["input"]["currency"] == "AUD"
    assert response.json["data"]["output"]["CZK"] is not None
    assert len(response.json["data"]["output"]) == 1


def test_convert_raises_single(client):
    response = client.get(
        "/api/currency_converter?"
        "amount=10&input_currency=agagahafasf&output_currency=Kč"
    )
    assert response.status_code == 400
    assert response.json == {
        "status": "bad_request",
        "message": "Unable to convert from agagahafasf to CZK",
    }


def test_convert_raises_all(client):
    response = client.get(
        "/api/currency_converter?" "amount=10&input_currency=agagahafasf"
    )
    assert response.status_code == 400
    assert response.json == {
        "status": "bad_request",
        "message": "Unable to calculate result from agagahafasf",
    }
