from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

from .core.config import config


SQL_DB_URL = config.db_url

engine = create_engine(SQL_DB_URL, connect_args={
    "check_same_thread" : False
}, echo=True)


class Base(DeclarativeBase):
    ...
    

class BaseModel(Base):
    __abstract__ = True
    
    id: Mapped[int] = mapped_column(primary_key=True)

session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db():
    db = session_local()
    
    try:
        yield db
    finally:
        db.close()