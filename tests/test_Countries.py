import pytest
from resources.Countries import *


def test_countries_resource_args(client):
    response = client.get("/api/countries?name=Slovak")
    assert response.status_code == 200
    assert response.json["data"][0]["name"] == "Slovakia"
    assert response.json["data"][0]["currencies"][0]["code"] == "EUR"


def test_countries_resource(client):
    response = client.get("/api/countries")
    assert response.status_code == 200
    assert response.json["data"][0]["name"] == "Afghanistan"
    assert response.json["data"][-1]["name"] == "Zimbabwe"


def test_not_found(client):
    response = client.get("/api/countries?name=FooBar")
    assert response.status_code == 404
    assert response.json == {
        "status": "not_found",
        "message": "Country not found",
    }


def test_bad_arg(client):
    response = client.get("/api/countries?arg=Foo")
    assert response.status_code == 400
    assert response.json == {"message": "Unknown arguments: arg"}


def test_empty_response(client):
    response = client.get("/api/countries?name=FooBar")
    assert response.status_code == 404
    assert response.json == {
        "status": "not_found",
        "message": "Country not found",
    }

