from requests_html import HTMLSession
import json


session = HTMLSession()


base_url = "https://restcountries.eu/rest/v2/"
payload = {"fields": "name;capital;alpha3Code;currencies"}
r = session.get(base_url + "all", params=payload).json()
output = json.dumps(r, indent=4, sort_keys=True, ensure_ascii=False)


def generateFile(data):
    with open(
        "./utils/countries_currencies.json", "w", encoding="utf-8"
    ) as outfile:
        outfile.write(data)


generateFile()
