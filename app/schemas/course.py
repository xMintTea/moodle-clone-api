from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional

from ..utils.schemas_utils import optional
from .user import UserResponse
from ..models.context.enums import Visibility
from .sections import SectionResponse


# -------- Course --------

class CourseBase(BaseModel):
    name: Annotated[str, Field(...,min_length=4, max_length=256)]
    description: Annotated[Optional[str], Field()]
    secret: Annotated[Optional[str], Field()]
    visibility: Annotated[Visibility, Field(default=Visibility.VISIBLE_TO_CREATOR)]



class CourseCreate(CourseBase):
    ...
    
@optional
class CourseUpdate(CourseBase):
    ...



class CourseResponce(CourseBase):
    id: int
    users: list[UserResponse]
    teachers: list[UserResponse]
    assistants: list[UserResponse]
    students: list[UserResponse]
    sections: list[SectionResponse]
    
    model_config = ConfigDict(from_attributes=True)

