from typing import List, Any
from database import db_connection
from models import GetInvoice, GetPerson, UserRoles, Tables


async def new_record(table: str, model_dump: dict[str, Any]):
    """
    Create a new record in database.
    :param table: Target table name
    :param model_dump: Dump of the pydantic model with input values
    :return: None
    """
    query = (f"INSERT INTO {table} ({', '.join(model_dump.keys())}) "
             f"VALUES ({', '.join([f':{field}' for field in model_dump.keys()])})")
    return await db_connection.execute(query, model_dump)


async def select_invoices(invoice: GetInvoice) -> List[dict[str, Any]]:
    """
    Select invoices records from database according to input params.
    :param invoice: Pydantic model with params to search
    :return: Unpacked selection result
    """
    query = f"SELECT * FROM {Tables.invoices} WHERE 1=1"
    order = f" ORDER BY (date_created, invoice_number) DESC"

    for field, value in invoice.model_dump(exclude_none=True).items():
        if field == "dates_interval":
            query += f" AND date_created >= NOW() - INTERVAL '{value} days'"
        elif field == 'limit':
            order += f' LIMIT {value}'
        else:
            query += f" AND {field} = '{value}'"
    query += order
    return [GetInvoice(**dict(row)).model_dump(exclude={'dates_interval', 'limit'})
            for row in await db_connection.fetch_all(query)]


async def select_persons(person: GetPerson) -> List[dict[str, Any]]:
    """
    Select persons records from database according to input params.
    :param person: Pydantic model with params to search
    :return: Unpacked selection result
    """
    inner_query = "SELECT *, '{role}' AS role FROM {table}"
    outer_query = "SELECT * FROM ({inner_query}) AS un WHERE 1=1"
    order = f" ORDER BY role DESC"
    if person.role is None:
        inner_query = (f"{inner_query.format(role=UserRoles.client, table=Tables.clients)} UNION "
                       f"{inner_query.format(role=UserRoles.manager, table=Tables.managers)}")
    else:
        table = Tables.clients if person.role == UserRoles.client else Tables.managers
        inner_query = inner_query.format(role=person.role, table=table)

    for field, value in person.model_dump(exclude_none=True, exclude={'role'}).items():
        if field == 'limit':
            order += f' LIMIT {value}'
        else:
            outer_query += f" AND {field} = '{value}'"
    outer_query += order
    print(outer_query)
    return [GetPerson(**dict(row)).model_dump(exclude={'limit'})
            for row in await db_connection.fetch_all(outer_query.format(inner_query=inner_query))]
