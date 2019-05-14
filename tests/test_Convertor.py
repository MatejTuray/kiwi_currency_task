import pytest
from utils.Convertor import Convertor

cnv = Convertor()


def test_get_single_rate(input_currency="EUR", output_currency="USD"):
    result = cnv.get_single_rate(input_currency, output_currency)
    assert result is not None


def test_raise_exception_single(input_currency="foo", output_currency="bar"):
    with pytest.raises(ValueError):
        assert cnv.get_single_rate(input_currency, output_currency)


def test_get_all_rates():
    result = cnv.get_all_rates()
    assert result is not None


def test_calculate(amount=10, input_currency="EUR", output_currency="USD"):
    result = cnv.calculate(
        amount,
        input_currency,
        output_currency,
        rate=cnv.get_single_rate("EUR", "USD"),
    )
    assert result["input"]["amount"] == amount
    assert result["input"]["currency"] == input_currency
    assert result["output"]["USD"] is not None
    assert len(result["output"]) == 1


def test_calculate_raises(
    amount=10, input_currency="saasdd", output_currency="gdgdsdhh"
):
    with pytest.raises(ValueError):
        assert cnv.calculate(
            amount,
            input_currency,
            output_currency,
            cnv.get_single_rate(input_currency, output_currency),
        )


def test_calculate_all(amount=10, input_currency="USD"):
    result = cnv.calculate_all(amount, input_currency, cnv.get_all_rates())
    assert result["input"]["amount"] == amount
    assert result["input"]["currency"] == input_currency
    assert "USD" not in result["output"]
    assert len(result["output"]) > 20


def test_calculate_all_raises(amount=10, input_currency="saasdd"):
    with pytest.raises(ValueError):
        assert cnv.calculate_all(amount, input_currency, cnv.get_all_rates())
