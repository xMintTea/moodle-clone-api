from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional
from datetime import datetime

from ..utils.schemas_utils import optional
from ..models.context.enums import Visibility


# -------- Pages --------

class PageBase(BaseModel):
    title: Annotated[str, Field()]
    description: Annotated[Optional[str], Field()]
    order: Annotated[int, Field(..., ge=0)]
    visibility: Annotated[Visibility, Field(default=Visibility.VISIBLE_TO_CREATOR)]
    due_date: Annotated[Optional[datetime], Field()]
    max_points: Annotated[int, Field()]



class PageCreate(PageBase):
    section_id: Annotated[int, Field(..., ge=1)]

@optional
class PageUpdate(PageCreate):
    ...


class PageResponse(PageBase):
    id: int
    section_id: Annotated[int, Field(..., ge=1)]
    creation_date: Annotated[datetime, Field(...)]
    last_change_date: Annotated[Optional[datetime], Field()]
    visibility: Visibility

    
    model_config = ConfigDict(from_attributes=True)