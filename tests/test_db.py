from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models.user import User
from app.models.course import Course, CourseSection, SectionContent, SectionPage


SQL_DB_URL = "sqlite:///:memory:"
engine = create_engine(
    SQL_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
Base.metadata.create_all(bind=engine)

TestingSessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)





