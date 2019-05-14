from requests_html import HTMLSession
import json
from datetime import datetime


session = HTMLSession()


base_url = "https://restcountries.eu/rest/v2/"
payload = {"fields": "name;capital;alpha3Code;currencies"}
r = session.get(base_url + "all", params=payload).json()


date = datetime.today().strftime("%Y-%m-%d")
url = f"https://api.cuex.com/v1/cubes/{date}?l=en"
cube = session.get(url).json()["data"]

currency_list = list(map(lambda x: x["currency"], cube))

for el in r:
    for element in el["currencies"]:
        try:
            if (
                element["code"] is not None
                and element["code"] not in currency_list
            ):
                try:
                    el["currencies"].remove(element)
                except KeyError:
                    print(element["code"] + " not found")
            elif element["code"] not in currency_list:
                try:
                    el["currencies"].remove(element)
                except KeyError:
                    print(element["code"] + " not found")
        except KeyError as e:
            print(e)

output = json.dumps(r, indent=4, sort_keys=True, ensure_ascii=False)


def generateFile(data):
    with open("./countries_currencies.json", "w", encoding="utf-8") as outfile:
        outfile.write(data)


generateFile(output)
