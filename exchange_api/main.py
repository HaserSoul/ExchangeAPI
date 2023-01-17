from fastapi import FastAPI, Depends, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from authorization import authorize_key
import routers.exchange_route.router as exchange_router
import routers.history_route.router as history_router
import routers.currencies_route.router as currencies_route


app = FastAPI(
    title="EXCHANGE RATES API",
    version="0.1.0",
    docs_url="/api-doc",
    redoc_url="/redoc",
)

app.include_router(router=exchange_router.router, dependencies=[Depends(authorize_key)])
app.include_router(router=currencies_route.router, dependencies=[Depends(authorize_key)])
app.include_router(router=history_router.router, dependencies=[Depends(authorize_key)])


@app.get("/", tags=["Info"])
async def informations():
    return {
        "name": app.title,
        "version": app.version,
        "message": f"See documentation at {app.docs_url}",
    }

if __name__ == "__main__":
    pass