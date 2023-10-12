import atexit
import os

from sqlalchemy import Column, DateTime, Integer, Text, String, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DB_USER = os.getenv("DB_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


PG_DSN = f"postgresql://{DB_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(PG_DSN)
atexit.register(engine.dispose)


Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)


class Advertisements(Base):
    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False, index=True)
    description = Column(Text, nullable=False)
    creation_time = Column(DateTime, server_default=func.now())
    creator = Column(String(25), nullable=False, index=True)


Base.metadata.create_all()

