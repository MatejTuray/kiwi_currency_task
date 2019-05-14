# kiwi_currency_converter

[![Build Status](https://travis-ci.org/MatejTuray/kiwi_currency_task.svg?branch=master)](https://travis-ci.org/MatejTuray/kiwi_currency_task)
![CI](https://img.shields.io/badge/Travis-red.svg?style=flat&logo=travis)
[![forthebadge made-with-python](https://img.shields.io/badge/made%20with-python-blue.svg?style=flat-square)](https://www.python.org/)
[![Codecov](https://codecov.io/gh/MatejTuray/kiwi_currency_task/branch/master/graph/badge.svg)](https://codecov.io/gh/MatejTuray/kiwi_currency_task)

```bash
git clone https://github.com/MatejTuray/kiwi_currency_task.git
```

```bash
docker-compose up -d
```

Easiest way to run cli while network is running:

```bash
docker-compose exec flask_api python cli.py --amount=100 --input_currency=¥ --output_currency=$
```

CLI handles symbols with multiple currencies by prompting the user to specify currency

![image](https://i.imgur.com/giSvImC.png)

API comes with interactive Swagger UI: `/api/docs` endpoint

## Parameters

- `amount` - amount which we want to convert - float
- `input_currency` - input currency - 3 letters name or currency symbol
- `output_currency` - requested/output currency - 3 letters name or currency symbol

## Functionality

- if output_currency param is missing, convert to all known currencies

## Output

- json

```

```
