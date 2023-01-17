from fastapi import APIRouter, Depends
from .services import ExchangeRates
from .validators import validate_exchange_input
from fastapi import HTTPException, status
from models import ExchangeModel

router = APIRouter(
    prefix="",
    tags=["Exchange"],
    responses={404: {"description": "Not found"}},
)


@router.get("/convert", tags=["Exchange"], response_model=ExchangeModel)
async def get_exchange_rate(
    parameters: dict = Depends(validate_exchange_input)
):
    code_from, code_to, amount = parameters
    return ExchangeRates().request_for_exchange(exchange_from=code_from, exchange_to=code_to, amount=amount)

