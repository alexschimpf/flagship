FROM python:3.12

WORKDIR /admin

COPY ./requirements.txt /admin/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /admin/requirements.txt

COPY ./app /admin/app
COPY ./config /admin/config

ENV PYTHONPATH=/admin

CMD uvicorn app.main:app --host 0.0.0.0 --port 80
