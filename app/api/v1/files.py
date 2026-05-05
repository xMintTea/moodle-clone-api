from fastapi import Depends
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.routing import APIRouter

from ...schemas.files import FileResponse
from ...resources.files import (
    create_file_dependency,
    get_file_dependency,
    stream_file_dependency
    )

router = APIRouter(prefix="/files", tags=["Files"])


@router.post("/", response_model=FileResponse)
def upload_file(
    file = Depends(create_file_dependency())
    ):
    return file


@router.get("/{file_id}", response_model=FileResponse)
def get_file(
    file = Depends(get_file_dependency()) 
):
    return file




@router.get("/{file_id}/stream")
def stream_file(
    file_stream = Depends(stream_file_dependency())
) -> StreamingResponse:
    return file_stream

