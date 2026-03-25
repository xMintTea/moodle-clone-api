from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional
from datetime import datetime

from ..utils.schemas_utils import optional
from .user import UserResponse
from .pages import PageResponse
from ..schemas.files import FileResponse


class PageSubmissionBase(BaseModel):
    user_id: Annotated[int, Field(...,ge=1)]


class PageSubmissionCreate(PageSubmissionBase):
    comment: Annotated[Optional[str], Field()]
    

@optional
class PageSubmissionUpdate(PageSubmissionBase):
    submitted: Annotated[bool, Field(default=False)]
    reviewed: Annotated[bool, Field(default=False)]
    points: Annotated[Optional[int], Field(default=0)]
    feedback: Annotated[Optional[str], Field()]


class PageSubmissionResponse(PageSubmissionBase):
    id: Annotated[int, Field()]
    points: Annotated[int, Field()]
    submittion_date: Annotated[datetime, Field(...)]    
    reviewed_date: Annotated[Optional[datetime], Field()]
    submitted: Annotated[bool, Field()]
    files: Annotated[list[FileResponse], Field()]
    feedback: Annotated[Optional[str], Field()]

    model_config = ConfigDict(from_attributes=True)

