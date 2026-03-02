from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import EmailStr

from database import BaseModel
from models.context.enums import UserStatus, UserType



class User(BaseModel):
    __tablename__ = "users"
    
    first_name: Mapped[str] = mapped_column(String(50))
    middle_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[EmailStr] = mapped_column(String(), unique=True)
    password: Mapped[str]
    salt: Mapped[str]   
    user_type: Mapped[UserType] = mapped_column(Enum(UserType))
    user_status: Mapped[UserStatus] = mapped_column(Enum(UserStatus))
    

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name} {self.middle_name}"
    