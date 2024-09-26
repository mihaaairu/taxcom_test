import os
from dotenv import load_dotenv
from databases import Database

load_dotenv()

db_connection = Database(f"postgresql+asyncpg://"
                         f"{os.environ['POSTGRES_USER']}:"
                         f"{os.environ['POSTGRES_PASSWORD']}@db:5432/"
                         f"{os.environ['POSTGRES_DB']}")
