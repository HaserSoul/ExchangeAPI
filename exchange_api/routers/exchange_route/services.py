import requests
import os
from fastapi import HTTPException, status
import datetime
import pytz
from database import ElasticConnection

class ElasticOperations(ElasticConnection):
    def __init__(self, credential_url: str) -> None:
        super().__init__(credential_url)

    def save_api_call(self, body: dict):
        index_exist = self.es_server.indices.exists(index="exchange-api-calls-history")
        if not index_exist:
            self.es_server.indices.create(index="exchange-api-calls-history")
        self.es_server.index(index="exchange-api-calls-history", doc_type="_doc", body=body)

class ExchangeRates:
    def __init__(self) -> None:
        self.exchange_auth_key = os.getenv("XE_EXCHANGE_AUTH")

    @staticmethod
    def get_date():
        timezone = "Europe/Warsaw"
        date = datetime.datetime.now(tz=pytz.timezone(timezone))

        return date

    def calculate_exchange(self, amount: float, rate: float) -> str:
        return str(round((amount*rate), 5))
    
    def request_for_exchange(self, exchange_from: str, exchange_to: str, amount: float):
        headers = {
        "authorization": self.exchange_auth_key
        }
        res = requests.get(f"https://www.xe.com/api/protected/statistics/?from={exchange_from}&to={exchange_to}", headers=headers)

        result: dict = res.json()

        if 'errorMessage' in result.keys():
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error. Contact with administrator",
        )

        rate = result.get('last1Days', {}).get('average')

        converted_amount = self.calculate_exchange(amount=amount, rate=rate)

        data = {
            "converted_amount": converted_amount,
            "rate": rate,
            "metadata": {
                "time_of_conversion": ExchangeRates.get_date(),
                "from_currency": exchange_from,
                "to_currency": exchange_to
            }
        }

        ElasticOperations(os.getenv("ES")).save_api_call(body=data)
        
        return data
