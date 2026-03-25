from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional
from datetime import datetime


class FileBase(BaseModel):
    id: Annotated[int, Field()]
    file_name: Annotated[str, Field()]
    content_type: Annotated[str, Field()]
    # headers: Mapped[str]
    size: Annotated[int, Field()]
    # file_bytes: Annotated[bytes, Field()]


class FileResponse(FileBase):
    model_config = ConfigDict(from_attributes=True)