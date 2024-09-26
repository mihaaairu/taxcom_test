from fastapi import APIRouter, Depends, responses
from fastapi.encoders import jsonable_encoder

from models import GetInvoice, NewInvoice, Tables
from database.db_api import select_invoices, new_record

invoices_router = APIRouter(prefix='/invoice')


@invoices_router.post('', tags=["invoice"], description='Select invoices from database according to input params')
async def get_invoices(invoice: GetInvoice = Depends()) -> responses.JSONResponse:
    invoices = await select_invoices(invoice)
    return responses.JSONResponse(
        status_code=200,
        content=jsonable_encoder({"invoices": invoices}),
    )


@invoices_router.put('', tags=["invoice"], description='Create new invoice in database with input params')
async def create_invoice(new_invoice: NewInvoice = Depends()) -> responses.JSONResponse:
    model_dump = new_invoice.model_dump(include_private=True)
    await new_record(Tables.invoices, model_dump)
    return responses.JSONResponse(
        status_code=200,
        content=jsonable_encoder({"message": f"Invoice created",
                                  "parameters": model_dump}),
    )
