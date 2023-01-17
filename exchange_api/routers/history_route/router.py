from fastapi import APIRouter
from database import ElasticConnection
import os
from models import ExchangeListModel

router = APIRouter(
    prefix="",
    tags=["Exchange"],
    responses={404: {"description": "Not found"}},
)


@router.get("/history", tags=["Exchange"], response_model=ExchangeListModel)
async def get_api_calls_history():
    query = {
        "query": {
            "match_all": {}
        }
        }
    return ElasticConnection(credential_url=os.getenv("ES")).get_api_calls(index='exchange-api-calls-history', query=query)

