from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional
from datetime import datetime

from ..utils.schemas_utils import optional
from .questions import Question
from ..models.context.enums import Visibility


class VideoBase(BaseModel):
    title: Annotated[str, Field(...)]
    description: Annotated[Optional[str], Field()]
    order: Annotated[int, Field(..., ge=0)]
    visibility: Annotated[Visibility, Field(default=Visibility.VISIBLE_EVERYONE)]
    video_url: Annotated[str, Field(...)]
    section_id: Annotated[int, Field(...)]

class VideoCreate(VideoBase):
    ...

@optional
class VideoUpdate(VideoCreate):
    ...
    

class VideoResponse(VideoBase):
    id: Annotated[int, Field(..., ge=1)]
    
    model_config = ConfigDict(from_attributes=True)