import json
from models import Country
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from config import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI)

with open(
    "./utils/countries_currencies.json", "r", encoding="utf8"
) as read_file:
    data = json.loads(read_file.read())

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
bulk_import = []

for item in data:
    capital = item["capital"]
    if item["capital"] == "":
        capital = "No capital"

    ctr = Country(
        name=item["name"],
        alpha3Code=item["alpha3Code"],
        capital=capital,
        currencies=item["currencies"],
    )
    bulk_import.append(ctr)

try:
    session.bulk_save_objects(bulk_import)
    session.commit()
except SQLAlchemyError as e:
    print(e)
finally:
    session.close()
