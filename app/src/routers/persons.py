from fastapi import APIRouter, Depends, responses
from fastapi.encoders import jsonable_encoder

from models import NewPerson, GetPerson, UserRoles, Tables
from database.db_api import select_persons, new_record

person_router = APIRouter(prefix='/person')


@person_router.post('', tags=["person"], description='Select persons from database according to input params')
async def get_persons(person: GetPerson = Depends()) -> responses.JSONResponse:
    persons = await select_persons(person)
    return responses.JSONResponse(
        status_code=200,
        content=jsonable_encoder({"persons": persons}),
    )


@person_router.put('', tags=["person"], description='Create new person in database with input params')
async def create_person(person: NewPerson = Depends()) -> responses.JSONResponse:
    table = Tables.clients if person.role == UserRoles.client else Tables.managers
    model_dump = person.model_dump(include_private=True, exclude={'role'})
    await new_record(table, model_dump)
    return responses.JSONResponse(
        status_code=200,
        content=jsonable_encoder({"message": f"New {person.role} created: {model_dump}"}),
    )

