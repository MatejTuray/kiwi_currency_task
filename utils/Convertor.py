from requests_html import HTMLSession
from datetime import datetime

session = HTMLSession()


class Convertor:
    """Fetches rates from cuex.com and calculates output currency"""

    def __init__(self, base_url="https://api.cuex.com/v1/exchanges/"):
        self.base_url = base_url

    def get_single_rate(self, input_currency, output_currency):
        """
        :param input_currency:Input currency to convert from
         - in ISO currency code
        :param output_currency: Output currency to convert to
        - in ISO currency code
        :return: Returns currency exchange rate for specified currency pair
        """

        url = self.base_url + input_currency.lower()
        payload = {
            "to_currency": output_currency.lower(),
            "from_date": datetime.today().strftime("%Y-%m-%d"),
            "l": "en",
        }
        try:
            r = session.get(url, params=payload).json()
            rate = r["data"][0]["rate"]
            return rate
        except Exception:
            raise ValueError(
                f"Invalid currencies provided: {input_currency},"
                f"{output_currency}"
            )

    def get_all_rates(self):
        """
        :return: Returns exchange rates for all currencies available,
        base currency is EUR
        """
        date = datetime.today().strftime("%Y-%m-%d")
        url = f"https://api.cuex.com/v1/cubes/{date}?l=en"
        try:
            rates = session.get(url).json()["data"]
            return rates
        except Exception:
            raise Exception("Unable to connect")

    def calculate_all(self, amount, input_currency, rates):
        """
        :param amount:Amount of money to convert 
        :param input_currency: Input currency to convert from
         - in ISO currency code 
        :param rates: Rates returned from get_all_rates method
        :return: Calculation is done by converting input currency to EUR first,
        and then to all available currencies,
        returns dictionary with the results
        """
        try:
            eur_rate = self.get_single_rate(input_currency.upper(), "EUR")
            input_in_eur = float(amount) * float(eur_rate)
            output = {}
            for curr in rates:
                if (
                    curr["currency"] == "EUR"
                    or curr["currency"] == input_currency.upper()
                ):
                    pass
                else:
                    output[f"{curr['currency']}"] = input_in_eur * float(
                        curr["rate"]
                    )
            result = {
                "input": {
                    "amount": amount,
                    "currency": input_currency.upper(),
                },
                "output": output,
            }
            return result
        except Exception:
            raise ValueError(
                f"Unable to calculate result from {input_currency}"
            )

    def calculate(self, amount, input_currency, output_currency, rate):
        """
        :param amount: Amount of money to convert 
        :param input_currency: Input currency to convert from
         - in ISO currency code
        :param output_currency: Ouput currency to convert to
         - in ISO currency code
        :param rate: Rates returned from get_single_rate method
        :return: Calculation is done by converting input currency to EUR first,
        and then to all available currencies,
        returns dictionary with the results
        """
        try:
            result = {
                "input": {
                    "amount": amount,
                    "currency": input_currency.upper(),
                },
                "output": {
                    output_currency.upper(): float(float(amount) * float(rate))
                },
            }
            return result
        except Exception as e:
            print(e)
            raise ValueError(
                f"Unable to convert between {input_currency}"
                f"and {output_currency}"
            )

