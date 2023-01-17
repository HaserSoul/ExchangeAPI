from fastapi import APIRouter
from .services import Scrapper
from models import CurrenciesModel

router = APIRouter(
    prefix="",
    tags=["Exchange"],
    responses={404: {"description": "Not found"}},
)

@router.get("/currencies", tags=["Exchange"], response_model=CurrenciesModel)
async def get_currencies():
    return Scrapper(url='https://www.xe.com/currency').get_currencies()
