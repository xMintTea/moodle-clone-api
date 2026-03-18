from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Annotated, Optional
from datetime import datetime

from ..utils.schemas_utils import optional
from .user import UserResponse
from ..models.context.enums import CourseAccessStatus, CourseAccessLevel

# -------- Course's user schemas --------

class CourseUserBase(BaseModel):
    access_level: Annotated[CourseAccessLevel, Field(default=CourseAccessLevel.STUDENT)]
    access_status: Annotated[CourseAccessStatus, Field(default=CourseAccessStatus.GRANTED)]


class CreateCourseUser(CourseUserBase):
    user_id: Annotated[int, Field(..., ge=1)]


@optional
class UpdateCourseUser(CourseUserBase):
    ...
    


class CourseUserResponse(CourseUserBase):
    user_id: Annotated[int, Field(..., ge=1)]
    course_id: Annotated[int, Field(..., ge=1)]
    date_of_join: Annotated[datetime, Field(...)]
    
    model_config = ConfigDict(from_attributes=True)