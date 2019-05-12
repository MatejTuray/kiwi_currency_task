FROM python:3.7-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk --no-cache add musl-dev linux-headers g++ postgresql-dev python3-dev openblas-dev libxml2-dev libxslt-dev libffi-dev libevent-dev

RUN pip install psycopg2-binary

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

RUN chmod 644 run.py
CMD ["python", "run.py"]