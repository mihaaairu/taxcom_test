from fastapi import FastAPI, Request, responses
from fastapi.encoders import jsonable_encoder
from contextlib import asynccontextmanager
from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError
from pydantic import ValidationError

from routers.invoices import invoices_router
from routers.persons import person_router
from models import openapi_tags_metadata
from database import db_connection


@asynccontextmanager
async def lifespan(app_: FastAPI):
    await db_connection.connect()
    yield
    await db_connection.disconnect()


app = FastAPI(lifespan=lifespan, openapi_tags=openapi_tags_metadata)
app.include_router(invoices_router)
app.include_router(person_router)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return responses.JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": exc.errors(include_url=False, include_context=False)}),
    )


@app.exception_handler(ForeignKeyViolationError)
async def validation_exception_handler(request: Request, exc: ForeignKeyViolationError):
    return responses.JSONResponse(
        status_code=500,
        content=jsonable_encoder({"severity": exc.as_dict().get('severity'),
                                  'detail': exc.as_dict().get('detail')}),
    )


@app.exception_handler(UniqueViolationError)
async def validation_exception_handler(request: Request, exc: ForeignKeyViolationError):
    return responses.JSONResponse(
        status_code=500,
        content=jsonable_encoder({"severity": exc.as_dict().get('severity'),
                                  'detail': exc.as_dict().get('detail')}),
    )
