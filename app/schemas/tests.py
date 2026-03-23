from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional
from datetime import datetime

from ..utils.schemas_utils import optional


# -------- Test --------

class TestBase(BaseModel):
    deadline_date: Annotated[Optional[datetime], Field()] = None
    order: Annotated[int, Field(..., ge=0)]
    visibility_id: Annotated[int, Field(..., ge=1)]


class TestCreate(TestBase):
    section_id: Annotated[int, Field(..., ge=1)]

@optional
class TestUpdate(TestCreate):
    ...
    

class TestResponse(TestBase):
    id: Annotated[int, Field(..., ge=1)]
    section_id: Annotated[int, Field(..., ge=1)]
    creation_date: Annotated[datetime, Field(...)]
    last_change_date: Annotated[Optional[datetime], Field()]

    model_config = ConfigDict(from_attributes=True)
