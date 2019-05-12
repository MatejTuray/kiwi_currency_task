#!/bin/bash

python migrate.py db init &&
python migrate.py db migrate &&
python migrate.py db upgrade &&
python seed.py
python -m pytest --cov-report term-missing --cov=.
python run.py
