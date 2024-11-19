from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from src.config import get_database_url

DATABASE_URL = get_database_url()
Base = declarative_base()
engine = create_engine(DATABASE_URL)

session_factory = sessionmaker(bind=engine, expire_on_commit=False)
