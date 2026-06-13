from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional
from datetime import datetime

from ..utils.schemas_utils import optional
from .questions import Question
from ..models.context.enums import Visibility
from .files import FileResponse


class ResourceBase(BaseModel):
    title: Annotated[str, Field(...)]
    description: Annotated[Optional[str], Field()]
    order: Annotated[int, Field(..., ge=0)]
    visibility: Annotated[Visibility, Field(default=Visibility.VISIBLE_EVERYONE)]

    

class ResourceCreate(ResourceBase):
    section_id: Annotated[int, Field(...,ge=1)]
    file_id: Annotated[int, Field(...,ge=1)]

@optional
class ResourceUpdate(ResourceCreate):
    ...
    

class ResourceResponse(ResourceBase):
    id: Annotated[int, Field(..., ge=1)]
    section_id: Annotated[int, Field(..., ge=1)]
    file: Annotated[FileResponse, Field()]
    
    model_config = ConfigDict(from_attributes=True)