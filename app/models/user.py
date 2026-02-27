from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import EmailStr

from database import BaseModel



class User(BaseModel):
    __tablename__ = "users"
    
    first_name: Mapped[str] = mapped_column(String(50))
    middle_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[EmailStr] = mapped_column(String())
    password: Mapped[str]
    salt: Mapped[str]
    user_type_id: Mapped[int] = mapped_column(ForeignKey("user_types.id"))
    user_status_id: Mapped[int] = mapped_column(ForeignKey("user_statuses.id"))
    
    
    user_type: Mapped["UserType"] = relationship()
    user_status: Mapped["UserStatus"] = relationship()
    

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name} {self.middle_name}"
    


class UserType(BaseModel):
    __tablename__ = "user_types"
    
    name: Mapped[str]


class UserStatus(BaseModel):
    __tablename__ = "user_statuses"
    
    name: Mapped[str]