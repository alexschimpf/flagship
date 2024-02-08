FROM python:3.12

WORKDIR /flags

COPY ./requirements.txt /flags/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /flags/requirements.txt

COPY ./app /flags/app
COPY ./config /flags/config

ENV PYTHONPATH=/flags

CMD uvicorn app.main:app --host 0.0.0.0 --port 80
