from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional
from datetime import datetime

from ..utils.schemas_utils import optional
from ..models.context.enums import Visibility
from .pages import PageResponse
from .tests import TestResponse
from .videos import VideoResponse
from .resources import ResourceResponse


# -------- Sections --------

class SectionBase(BaseModel):
    title: Annotated[str, Field(..., min_length=1, max_length=256)]
    description: Annotated[Optional[str], Field()] = None
    order: Annotated[int, Field(..., ge=0)]
    visibility: Annotated[Visibility, Field(default=Visibility.VISIBLE_TO_CREATOR)]


class SectionCreate(SectionBase):
    course_id: Annotated[int, Field(..., ge=1)]

@optional
class SectionUpdate(SectionCreate):
    ...


class SectionResponse(SectionBase):
    id: Annotated[int, Field()]
    course_id: Annotated[int, Field()]
    
    pages: list[PageResponse]
    tests: list[TestResponse]
    videos: list[VideoResponse]
    resources: list[ResourceResponse]
    
    model_config = ConfigDict(from_attributes=True)
