from sqlalchemy import String, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import EmailStr
from typing import Optional

from ..database import Base
from ..models.context.enums import UserStatus, UserType


class User(Base):
    __tablename__ = "users"
    
    first_name: Mapped[str] = mapped_column(String(50))
    middle_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[EmailStr] = mapped_column(String(), unique=True)
    password: Mapped[bytes]
    user_type: Mapped[UserType] = mapped_column(Enum(UserType))
    user_status: Mapped[UserStatus] = mapped_column(Enum(UserStatus))
    
    group_id: Mapped[Optional[int]] = mapped_column(ForeignKey("student_groups.id"), nullable=True)
    
    courses: Mapped[list["Course"]] = relationship(back_populates="users", secondary="course_users") # type: ignore
    group: Mapped[Optional["StudentGroup"]] = relationship(uselist=False)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name} {self.middle_name}"
    

    
    def __str__(self) -> EmailStr:
        return f"{self.full_name}[{self.id}]"
    
    
class StudentGroup(Base):
    __tablename__ = "student_groups"
    
    name: Mapped[str]
    
    users: Mapped[list[User]] = relationship(back_populates="group")