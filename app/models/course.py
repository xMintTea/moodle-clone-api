from sqlalchemy import String,Text, ForeignKey, DateTime, text, Enum, and_
from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr
from typing import Optional, List
from datetime import datetime

from ..database import Base
from ..models.user import User
from ..models.file import File
from ..models.context.enums import CourseAccessLevel, CourseAccessStatus, Visibility



class SectionContent(Base):
    __abstract__ = True
    
    title: Mapped[str]
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    creation_date: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )
    last_change_date: Mapped[Optional[datetime]]
    due_date: Mapped[Optional[datetime]]
    
    order: Mapped[int]
    visibility: Mapped[Visibility] = mapped_column(Enum(Visibility), default=Visibility.VISIBLE_TO_CREATOR)

    max_points: Mapped[int] = mapped_column(default=0)

    section_id: Mapped[int] = mapped_column(ForeignKey("course_sections.id", ondelete="CASCADE"))
   
class Course(Base):
    __tablename__ = "courses"
    
    name: Mapped[str] = mapped_column(String(256))
    description: Mapped[Optional[str]] = mapped_column(Text)
    
    creation_date: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )
    
    secret: Mapped[Optional[str]]
    visibility: Mapped[Visibility] = mapped_column(Enum(Visibility), default=Visibility.VISIBLE_TO_CREATOR)
    
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
    
    
    def __str__(self) -> str:
        return f"{self.name}[{self.id}]"


class CourseSection(Base):
    __tablename__ = "course_sections"
    
    title: Mapped[str] = mapped_column(String(256))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    order: Mapped[int]
    visibility: Mapped[Visibility] = mapped_column(Enum(Visibility), default=Visibility.VISIBLE_TO_CREATOR)
    
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"))
    
    pages: Mapped[list["SectionPage"]] = relationship(
        back_populates="section",
        cascade="all, delete-orphan"
    )
    tests: Mapped[list["Test"]] = relationship(
        back_populates="section",
        cascade="all, delete-orphan"
    )
    
    course: Mapped[Course] = relationship(back_populates="sections")


    def __str__(self) -> str:
        return f"{self.title}[{self.id}]"


class SectionPage(SectionContent):
    __tablename__ = "section_pages"
    
    comment: Mapped[Optional[str]] = mapped_column(Text)
    
    section: Mapped[CourseSection] = relationship(back_populates="pages")
    submitted_pages: Mapped[list["SubmittedPage"]] = relationship(back_populates="page") 
    
    files: Mapped[list[File]] = relationship(back_populates="pages", secondary="files_on_page")
    
    # TODO: Good for now. Gonna figure out later how to store page content there.
    
    
    def __str__(self) -> str:
        return f"{self.title}[{self.id}]"



class FilesOnPage(Base):
    __tablename__ = "files_on_page"
    
    file_id: Mapped[int] = mapped_column(ForeignKey("files.id"))
    page_id: Mapped[int] = mapped_column(ForeignKey("section_pages.id"))


class FilesOnSubmission(Base):
    __tablename__ = "files_on_submittion"
    
    file_id: Mapped[int] = mapped_column(ForeignKey("files.id"))
    submittion_id: Mapped[int] = mapped_column(ForeignKey("submitted_page.id"))


class SubmittedPage(Base):
    __tablename__ = "submitted_page"
    
    page_id: Mapped[int] = mapped_column(ForeignKey("section_pages.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    submitted: Mapped[bool]= mapped_column(default=True)
    submittion_date: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )
    comment: Mapped[Optional[str]] = mapped_column(Text)
    feedback: Mapped[Optional[str]] = mapped_column(Text)
    reviewed: Mapped[bool] = mapped_column(default=False)
    reviewed_date: Mapped[Optional[datetime]]
    points: Mapped[int] = mapped_column(default=0)
    
    page: Mapped[SectionPage] = relationship(back_populates="submitted_pages")
    user: Mapped[User] = relationship()
    
    files: Mapped[list[File]] = relationship(back_populates="submittions", secondary="files_on_submittion")


class Test(SectionContent):
    __tablename__ = "tests"
    
    deadline_date: Mapped[Optional[datetime]]
    
    section: Mapped[CourseSection] = relationship(back_populates="tests")


class TestResult(Base):
    __tablename__ = "test_results"
    
    test_id: Mapped[int] = mapped_column(ForeignKey("tests.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]
    answers: Mapped[str] = mapped_column(Text)

class CourseUser(Base):
    __tablename__ = "course_users"
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    access_level: Mapped[CourseAccessLevel] = mapped_column(Enum(CourseAccessLevel), default=CourseAccessLevel.STUDENT)
    access_status: Mapped[CourseAccessStatus] = mapped_column(Enum(CourseAccessStatus), default=CourseAccessStatus.GRANTED)
    date_of_join: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP")
    )
    
    user: Mapped["User"] = relationship(viewonly=True, overlaps="courses,users")
    course: Mapped[Course] = relationship(viewonly=True, overlaps="courses,users")


