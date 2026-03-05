from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Annotated

from ..models.context.enums import UserStatus, UserType




class UserBase(BaseModel):
    first_name: Annotated[str,Field(..., title="Имя пользователя",
                                    min_length=2,
                                    max_length=50)]
    middle_name: Annotated[str,Field(..., title="Отчество пользователя",
                                    min_length=2,
                                    max_length=50)]
    last_name: Annotated[str,Field(..., title="Фамилия пользователя",
                                    min_length=2,
                                    max_length=50)]


    user_type: Annotated[UserType, Field(...)]
    user_status: Annotated[UserStatus, Field(...)]


class UserCreate(UserBase):
    password: Annotated[str, Field(..., min_length=8, max_length=18)]
    email: Annotated[EmailStr, Field(..., max_length=32)]


class UserUpdate(UserCreate):
    ...


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)