from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Annotated, Optional
from datetime import datetime

from ..utils.schemas_utils import optional



# -------- Visibility --------

class VisibilityBase(BaseModel):
    name: Annotated[str, Field(...)]


# -------- Course --------

class CourseBase(BaseModel):
    name: Annotated[str, Field(...,min_length=4, max_length=256)]
    description: Annotated[Optional[str], Field()]
    secret: Annotated[Optional[str], Field()]
    visibility_id: Annotated[int, Field(..., ge=1)]



class CourseCreate(CourseBase):
    ...
    
@optional
class CourseUpdate(CourseBase):
    ...



class CourseResponce(CourseBase):
    model_config = ConfigDict(from_attributes=True)



# -------- Sections --------

class SectionBase(BaseModel):
    title: Annotated[str, Field(..., min_length=1, max_length=256)]
    description: Annotated[Optional[str], Field()] = None
    order: Annotated[int, Field(..., ge=0)]
    visibility_id: Annotated[int, Field(..., ge=1)]


class SectionCreate(SectionBase):
    course_id: Annotated[int, Field(..., ge=1)]

@optional
class SectionUpdate(SectionCreate):
    ...


class SectionResponse(SectionBase):
    id: Annotated[int, Field()]
    course_id: Annotated[int, Field()]
    
    model_config = ConfigDict(from_attributes=True)


# -------- Sections --------

class PageBase(BaseModel):
    order: Annotated[int, Field(..., ge=0)]
    visibility_id: Annotated[int, Field(..., ge=0)]



class PageCreate(PageBase):
    section_id: Annotated[int, Field(..., ge=1)]

@optional
class PageUpdate(PageCreate):
    ...


class PageResponse(PageBase):
    # TODO: gonna figure out how annotate this properly.
    section_id: int
    creation_date: datetime
    last_change_date: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)



# -------- Test --------

class TestBase(BaseModel):
    deadline_date: Annotated[Optional[datetime], Field()] = None
    order: Annotated[int, Field(..., ge=0)]
    visibility_id: Annotated[int, Field(..., ge=1)]


class TestCreate(TestBase):
    section_id: Annotated[int, Field(..., ge=1)]

@optional
class TestUpdate(TestCreate):
    ...
    

class TestResponse(TestBase):
    id: int
    section_id: int
    creation_date: datetime
    last_change_date: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
