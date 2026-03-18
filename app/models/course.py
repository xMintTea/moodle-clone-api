from sqlalchemy import String,Text, ForeignKey, DateTime, text, Enum, and_
from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr
from typing import Optional, List
from datetime import datetime

from ..database import BaseModel
from ..models.user import User
from ..models.context.enums import CourseAccessLevel, CourseAccessStatus, Visibility



class SectionContent(BaseModel):
    __abstract__ = True
    
    section_id: Mapped[int] = mapped_column(ForeignKey("course_sections.id", ondelete="CASCADE"))
    creation_date: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )
    last_change_date: Mapped[Optional[datetime]]
    order: Mapped[int]
    visibility: Mapped[Visibility] = mapped_column(Enum(Visibility), default=Visibility.VISIBLE_TO_CREATOR)
 


   
class Course(BaseModel):
    __tablename__ = "courses"
    
    name: Mapped[str] = mapped_column(String(256))
    description: Mapped[Optional[str]] = mapped_column(Text)
    secret: Mapped[Optional[str]]
    visibility: Mapped[Visibility] = mapped_column(Enum(Visibility), default=Visibility.VISIBLE_TO_CREATOR)
    creation_date: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )
    
    sections: Mapped[list["CourseSection"]] = relationship(
        back_populates="course",
        cascade="all, delete-orphan"
    )
    
    users: Mapped[List[User]] = relationship(back_populates="courses", secondary="course_users")

    teachers: Mapped[List[User]] = relationship(
        secondary="course_users",
        primaryjoin=lambda: and_(
            Course.id == CourseUser.course_id,
            CourseUser.access_level == CourseAccessLevel.TEACHER
        ),
        secondaryjoin=lambda: User.id == CourseUser.user_id,
        viewonly=True,
        overlaps="users"
    )
    
    
    assistants: Mapped[List[User]] = relationship(
        secondary="course_users",
        primaryjoin=lambda: and_(
            Course.id == CourseUser.course_id,
            CourseUser.access_level == CourseAccessLevel.ASSISTENT
        ),
        secondaryjoin=lambda: User.id == CourseUser.user_id,
        viewonly=True,
        overlaps="users"
    )
    
    students: Mapped[List[User]] = relationship(
        secondary="course_users",
        primaryjoin=lambda: and_(
            Course.id == CourseUser.course_id,
            CourseUser.access_level == CourseAccessLevel.STUDENT
        ),
        secondaryjoin=lambda: User.id == CourseUser.user_id,
        viewonly=True,
        overlaps="users"
    )


class CourseSection(BaseModel):
    __tablename__ = "course_sections"
    
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(256))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    order: Mapped[int]
    visibility: Mapped[Visibility] = mapped_column(Enum(Visibility), default=Visibility.VISIBLE_TO_CREATOR)
    
    pages: Mapped[list["SectionPage"]] = relationship(
        back_populates="section",
        cascade="all, delete-orphan"
    )
    tests: Mapped[list["Test"]] = relationship(
        back_populates="section",
        cascade="all, delete-orphan"
    )
    
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

class CourseUser(BaseModel):
    __tablename__ = "course_users"
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    access_level: Mapped[CourseAccessLevel] = mapped_column(Enum(CourseAccessLevel), default=CourseAccessLevel.STUDENT)
    access_status: Mapped[CourseAccessStatus] = mapped_column(Enum(CourseAccessStatus), default=CourseAccessStatus.GRANTED)
    date_of_join: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )
    
    user: Mapped["User"] = relationship()
    course: Mapped[Course] = relationship()


