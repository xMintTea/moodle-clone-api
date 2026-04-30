from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Annotated, Optional
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str
    model_config = ConfigDict(from_attributes=True)
    
class Login(BaseModel):
    email: EmailStr
    password: str