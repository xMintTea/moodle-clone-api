from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Annotated, Optional
from datetime import datetime

from ..utils.schemas_utils import optional
from .user import UserResponse
from ..models.context.enums import CourseAccessStatus, CourseUserType

# -------- Course's user schemas --------

class CourseUserBase(BaseModel):
    access_lvl: Annotated[CourseUserType, Field(default=CourseUserType.STUDENT)]
    access_status_id: Annotated[CourseAccessStatus, Field(default=CourseAccessStatus.GRANTED)]


class CreateCourseUser(CourseUserBase):
    ...


@optional
class UpdateCourseUser(CourseUserBase):
    ...
    


class CourseUserResponse(CreateCourseUser):
    user_id: Annotated[int, Field(..., ge=1)]
    course_id: Annotated[int, Field(..., ge=1)]
    date_of_join: Annotated[datetime, Field(...)]
    
    model_config = ConfigDict(from_attributes=True)