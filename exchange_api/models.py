from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime

class MetaDataModel(BaseModel):
    time_of_conversion: datetime
    from_currency: str
    to_currency: str

class ExchangeModel(BaseModel):
    converted_amount: str
    rate: float
    metadata: MetaDataModel

class CurrenciesModel(BaseModel):
    __root__: dict

class ExchangeListModel(BaseModel):
    __root__: List[ExchangeModel]
