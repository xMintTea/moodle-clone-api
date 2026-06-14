from fastapi import Depends, UploadFile, File as FileParam, Path
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy.exc import NoResultFound
from fastapi.responses import StreamingResponse

from ..database import get_db
from ..service.file_service import FileService
from ..security.authorization import get_verified_user
from ..models.user import User
from ..models.file import File as FileObject
from ..models.context.enums import UserType



def get_file_service(session: Session = Depends(get_db)):
    return FileService(session)


def create_file_dependency():
    def dependency(
        uploaded_file: UploadFile = FileParam(...),
        user: User = Depends(get_verified_user),
        file_service: FileService = Depends(get_file_service)
    ) -> FileObject:

        return file_service.create_file(uploaded_file, user.id)
    
    return dependency


def get_file_dependency():
    def dependency(
        file_id: Annotated[int, Path(ge=1)],
        file_service: FileService = Depends(get_file_service),
        user: User = Depends(get_verified_user)
    ) -> FileObject:
        
        file = file_service.get_file(file_id)
        
        if file is None:
            raise NoResultFound
        
        return file
    
    return dependency
    


def stream_file_dependency():
    def dependency(
        file_id: Annotated[int, Path(ge=1)],
        file_service: FileService = Depends(get_file_service),
        user: User = Depends(get_verified_user)
    ) -> StreamingResponse:
        file = file_service.get_file(file_id)
        file_stream = file_service.stream_file(file_id)
        
        if file is None:
            raise NoResultFound
        
        
        return file_stream
    
    return dependency