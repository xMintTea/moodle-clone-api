from sqlalchemy import String,Text, ForeignKey, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr
from typing import Optional, List
from datetime import datetime

from database import BaseModel
from models.user import User



class SectionContent(BaseModel):
    __abstract__ = True
    
    section_id: Mapped[int] = mapped_column(ForeignKey("course_sections.id", ondelete="CASCADE"))
    creation_date: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )
    last_change_date: Mapped[Optional[datetime]]
    order: Mapped[int]
    visibility_id: Mapped[int] = mapped_column(ForeignKey("visibility.id"))
    
    @declared_attr
    def visibility(self) -> Mapped["Visibility"]:
        return relationship()
 


   
class Course(BaseModel):
    __tablename__ = "courses"
    
    name: Mapped[str] = mapped_column(String(256))
    description: Mapped[Optional[str]] = mapped_column(Text)
    secret: Mapped[Optional[str]]
    visibility_id: Mapped[int] = mapped_column(ForeignKey("visibility.id"))
    creation_date: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )
    
    visibility: Mapped["Visibility"] = relationship()
    sections: Mapped[list["CourseSection"]] = relationship(
        back_populates="course",
        cascade="all, delete-orphan"
    ) 



class CourseSection(BaseModel):
    __tablename__ = "course_sections"
    
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(256))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    order: Mapped[int]
    visibility_id: Mapped[int] = mapped_column(ForeignKey("visibility.id"))
    
    pages: Mapped[list["SectionPage"]] = relationship(
        back_populates="section",
        cascade="all, delete-orphan"
    )
    tests: Mapped[list["Test"]] = relationship(
        back_populates="section",
        cascade="all, delete-orphan"
    )
    visibility: Mapped["Visibility"] = relationship()
    
    course: Mapped[Course] = relationship(back_populates="sections")



class SectionPage(SectionContent):
    __tablename__ = "section_pages"
    
    section: Mapped[CourseSection] = relationship(back_populates="pages")
    
    # TODO: Good for now. Gonna figure out later how to store page content there. 


class Test(SectionContent):
    __tablename__ = "tests"
    
    deadline_date: Mapped[Optional[datetime]]
    
    section: Mapped[CourseSection] = relationship(back_populates="tests")


class TestResult(BaseModel):
    __tablename__ = "test_results"
    
    test_id: Mapped[int] = mapped_column(ForeignKey("tests.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]
    answers: Mapped[str] = mapped_column(Text)


class Visibility(BaseModel):
    __tablename__ = "visibility"
    
    name: Mapped[str]


class CourseUser(BaseModel):
    __tablename__ = "course_users"
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    access_level_id: Mapped[int] = mapped_column(ForeignKey("access_levels.id"))
    access_status_id: Mapped[int] = mapped_column(ForeignKey("access_statuses.id"))
    date_of_join: Mapped[datetime]


class AccessLevel(BaseModel):
    __tablename__ = "access_levels"
    
    name: Mapped[str]


class AccessStatus(BaseModel):
    __tablename__ = "access_statuses"
    
    name: Mapped[str]
