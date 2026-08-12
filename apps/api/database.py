import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase


load_dotenv() # Load environment variables from .env file

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set. Did you create a .env file?")

engine = create_async_engine(DATABASE_URL, echo=True) #SQLAlchemy's core connection to the manager database

# A session is a single conversation with a database. It manages the persistence operations for ORM-mapped objects.
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)  #It creates new sessions whenever a route is needed to interact with the database.

class Base(DeclarativeBase):
  pass