from fastapi import Depends, status, Query, Path, UploadFile, File
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.routing import APIRouter
from typing import Optional, Annotated, List
from sqlalchemy.orm import Session

from ...database import get_db
from ...schemas.files import FileResponse
from ...service.file_service import FileService

router = APIRouter(prefix="/files", tags=["Files"])


def get_file_service(session: Session = Depends(get_db)) -> FileService:
    return FileService(session)

@router.post("/", response_model=FileResponse)
def upload_file(
    uploaded_file: UploadFile = File(...),
    file_service: FileService = Depends(get_file_service)
    ):
    return file_service.create_file(uploaded_file)


@router.get("/{file_id}", response_model=FileResponse)
def get_file(
    file_id: Annotated[int, Path(ge=1)],
    file_service: FileService = Depends(get_file_service)
):
    return file_service.get_file(file_id)


@router.get("/{file_id}/stream")
def stream_file(
    file_id: Annotated[int, Path(ge=1)],
    file_service: FileService = Depends(get_file_service)
):
    return file_service.stream_file(file_id)

