import uuid

from decimal import Decimal
from pydantic import BaseModel, Field, PrivateAttr, model_validator
from typing import Literal, Optional
from datetime import date
from dataclasses import dataclass
from fastapi import Query

SHIPMENT_STATUSES = Literal['NOT SHIPPED', 'PARTIALLY SHIPPED', 'SHIPPED']
PAYMENT_STATUSES = Literal['NOT PAID', 'PAID', 'PARTIALLY PAID', 'CANCELLED']

openapi_tags_metadata = [
    {
        "name": "invoice",
        "description": "Operations with invoices",
    },
    {
        "name": "person",
        "description": "Operations with persons"
    },
]


@dataclass
class Tables:
    clients = 'clients'
    managers = 'managers'
    invoices = 'invoices'


@dataclass
class UserRoles:
    type_ = Literal['CLIENT', 'MANAGER']
    client = 'CLIENT'
    manager = 'MANAGER'


class ExtendedDumpBaseModel(BaseModel):

    def model_dump(self, include_private: bool = False, **kwargs):
        model_dump = super().model_dump(**kwargs)
        if include_private:
            privacy_lost_attrs = {key.lstrip('_'): value for key, value in self.__pydantic_private__.items()}
            privacy_lost_attrs.update(**model_dump)
            model_dump = privacy_lost_attrs
        return model_dump


class NewInvoice(ExtendedDumpBaseModel):
    _invoice_id: uuid.UUID = PrivateAttr(default_factory=uuid.uuid4)
    _date_created: date = PrivateAttr(default_factory=date.today)

    manager_id: uuid.UUID = Field(Query(description='Existing manager unique ID'))
    client_id: uuid.UUID = Field(Query(description='Existing client unique ID'))
    amount: Decimal = Field(Query(decimal_places=2, description='Invoice amount'))
    payment_status: PAYMENT_STATUSES = Field(Query(description='Payment actual status'))
    shipment_status: SHIPMENT_STATUSES = Field(Query(description='Shipment actual status'))


class GetInvoice(BaseModel):
    invoice_id: Optional[uuid.UUID] = Field(Query(default=None, description='Invoice unique ID'))
    date_created: Optional[date] = Field(Query(default=None, description='Invoice creation date (YYYY-MM-DD)'))
    dates_interval: Optional[int] = Field(Query(default=None, ge=0, description='Invoices dates interval in days'))
    invoice_number: Optional[int] = Field(Query(default=None, ge=1,
                                                description='Invoice number (invoice local ID in scope of one day)'))
    limit: Optional[int] = Field(Query(default=20, ge=0,
                                       description='Limit of invoices. '
                                                   'Ordered DESC by date_created and invoice_number'))
    manager_id: Optional[uuid.UUID] = Field(Query(default=None, description='Manager unique ID'))
    client_id: Optional[uuid.UUID] = Field(Query(default=None, description='Client unique ID'))
    amount: Optional[Decimal] = Field(Query(default=None, decimal_places=2, description='Invoice amount'))
    payment_status: Optional[PAYMENT_STATUSES] = Field(Query(default=None, description='Payment actual status'))
    shipment_status: Optional[SHIPMENT_STATUSES] = Field(Query(default=None, description='Shipment actual status'))

    @model_validator(mode='before')
    def check_date_fields(cls, values):
        if (values.get('date_created') is not None) and (values.get('date_scope') is not None):
            raise ValueError('The date_created and date_scope fields are mutually exclusive. Fill in one of them')
        return values


class NewPerson(ExtendedDumpBaseModel):
    _id: uuid.UUID = PrivateAttr(default_factory=uuid.uuid4)
    name: str = Field(Query(description='Personal name'))
    role: UserRoles.type_ = Field(Query(description="Personal role"))


class GetPerson(BaseModel):
    id: Optional[uuid.UUID] = Field(Query(default=None, description='Personal unique ID'))
    name: Optional[str] = Field(Query(default=None, description='Personal name'))
    role: Optional[UserRoles.type_] = Field(Query(default=None, description="Personal role"))
    limit: Optional[int] = Field(Query(default=20, ge=0,
                                       description='Limit of invoices. '
                                                   'Ordered DESC by date_created and invoice_number'))
