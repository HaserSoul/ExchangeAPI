FROM python:3.9

WORKDIR /exchange_api

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r /exchange_api/requirements.txt

COPY exchange_api .

EXPOSE 8000

CMD [ "uvicorn",  "main:app", "--host", "0.0.0.0"]