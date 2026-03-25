from .database import Base, engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin

from .api.v1 import router as routerV1
from .core.register_exception_handlers import register_exception_handlers
from .admin import register_views

Base.metadata.create_all(engine)

app = FastAPI()
register_exception_handlers(app)

app.include_router(routerV1)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


admin = Admin(app, engine)
register_views(admin)