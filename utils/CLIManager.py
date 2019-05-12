from __future__ import print_function, unicode_literals
import re
import json
from PyInquirer import prompt, default_style


class CLIManager:
    """
    CLI manager class, input parsing and converting currencies
    """

    def __init__(self, convertor, session, url=""):
        self.cnv = convertor
        self.session = session
        self.url = url

    def parse_and_prompt(self, currency):
        """"
        :param currency:
        Currency to parse - if it isn't a ISO country
        code or unique currency symbol (i.e. Kč),
        prompts the user to select from list of currencies
        denominated by the same symbol
        :return:
        Returns ISO currency code
        """
        if re.match(r"[A-Z]{3}", currency, re.IGNORECASE) is None:
            res = self.session.get(
                f"{self.url}/api/symbols?symbol={currency}"
            ).json()
            if len(res["symbols"]) > 1:
                questions = [
                    {
                        "type": "list",
                        "name": "currency",
                        "message": f"Currency options for symbol - {currency}",
                        "choices": res["symbols"],
                        "filter": lambda val: val.lower(),
                    }
                ]

                answers = prompt(questions, style=default_style)
                return answers["currency"]
            else:
                return res["symbols"][0]["value"]
        else:
            return currency

    def calculate(self, amount, input_currency, output_currency):
        """
        Parses currencies with parse_and_prompt method and passes
        iso codes to Convertor class to calculate
        :param amount:
        Amount of money to convert
        :param input_currency:
        Input currency
        :param output_currency:
        Output currency
        :return:
        Returns json string with calculation output
        """
        if output_currency is None:
            input_currency = self.parse_and_prompt(input_currency)
            return json.dumps(
                self.cnv.calculate_all(
                    amount,
                    input_currency,
                    self.cnv.get_all_rates(amount, input_currency),
                ),
                indent=4,
                ensure_ascii=False,
            )
        else:
            input_currency = self.parse_and_prompt(input_currency)
            output_currency = self.parse_and_prompt(output_currency)
            return json.dumps(
                self.cnv.calculate(
                    amount,
                    input_currency,
                    output_currency,
                    self.cnv.get_single_rate(input_currency, output_currency),
                ),
                indent=4,
                ensure_ascii=False,
            )
