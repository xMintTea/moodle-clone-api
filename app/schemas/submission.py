from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional
from datetime import datetime

from ..utils.schemas_utils import optional
from .user import UserResponse
from .pages import PageResponse


class PageSubmissionBase(BaseModel):
    user_id: Annotated[int, Field(...,ge=1)]


class PageSubmissionCreate(PageSubmissionBase):
    ...
    

@optional
class PageSubmissionUpdate(PageSubmissionCreate):
    submitted: Annotated[bool, Field(default=False)]
    reviewed: Annotated[bool, Field(default=False)]
    points: Annotated[Optional[int], Field(default=0)]


class PageSubmissionResponse(PageSubmissionBase):
    page: Annotated[PageResponse, Field()]
    user: Annotated[UserResponse, Field()]
    points: Annotated[int, Field()]
    submittion_date: Annotated[datetime, Field(...)]    
    reviewed_date: Annotated[Optional[datetime], Field()]

    model_config = ConfigDict(from_attributes=True)

