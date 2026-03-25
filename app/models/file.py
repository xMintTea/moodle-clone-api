from sqlalchemy import String,Text, ForeignKey, DateTime, text, Enum, and_
from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr
from typing import Optional, List
from datetime import datetime

from ..database import Base


class File(Base):
    __tablename__ = "files"
    
    file_name: Mapped[str]
    content_type: Mapped[str]
    headers: Mapped[str]
    size: Mapped[int]
    file_bytes: Mapped[bytes]
    
    uploader_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    
    pages: Mapped[list["SectionPage"]] = relationship(back_populates="files", secondary="files_on_page")
    submittions: Mapped[list["SubmittedPage"]] = relationship(back_populates="files", secondary="files_on_submittion")