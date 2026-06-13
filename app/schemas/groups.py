from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional
from datetime import datetime

class GroupBase(BaseModel):
    name: Annotated[str, Field(...,min_length=2, max_length=100)]
    
    
class GroupCreate(GroupBase):
    ...


class GroupUpdate(GroupCreate):
    ...
    
    
class GroupResponse(GroupBase):
    id: Annotated[int, Field(ge=1)]