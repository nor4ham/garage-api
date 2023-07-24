from datetime import datetime

from sqlalchemy.orm import declarative_base, Session, sessionmaker
from sqlalchemy.future.engine import create_engine

from app.config import config

engine = create_engine(config.SQLALCHEMY_DATABASE_URL)
SessionLocal : Session = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)  # type: ignore

Base = declarative_base()
DELETE_DATETIME = datetime.fromtimestamp(0)
