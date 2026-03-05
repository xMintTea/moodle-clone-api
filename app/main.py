from .database import Base, engine
from fastapi import FastAPI

from .api.v1 import router as routerV1
from .core.register_exception_handlers import register_exception_handlers

Base.metadata.create_all(engine)

app = FastAPI()

