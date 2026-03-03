from pydantic import BaseModel, Field, EmailStr
from typing import Annotated, Optional

class CourseSchema(BaseModel):
    name: Annotated[str, Field(...,min_length=4, max_length=256)]
    description: Annotated[str, Field()]
    secret: Annotated[Optional[str], Field()]
    visibility_id: Annotated[int, Field(..., ge=1)]


class CourseSection(BaseModel):
    course_id: Annotated[int, Field(..., ge=1)]