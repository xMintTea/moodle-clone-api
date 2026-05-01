from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from datetime import datetime
from typing import Optional
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
import urllib.parse

from ..models.file import File


class FileService:
    def __init__(self, session: Session) -> None:
        self._db = session
    
    
    def create_file(self, uploaded_file: UploadFile, uploader_id: Optional[int] = None) -> File:
        
        bytes = uploaded_file.file.read()

        file = File(
            file_name=uploaded_file.filename,
            content_type=uploaded_file.content_type,
            headers=str(dict(uploaded_file.headers)),
            size=uploaded_file.size,
            file_bytes=bytes,
            uploader_id=uploader_id
        )
        
        self._db.add(file)
        self._db.commit()
        self._db.refresh(file)
        
        return file
    
    
    def get_file(self, file_id: int) -> Optional[File]:
        return self._db.get(File, file_id)
    
    
    def stream_file(self, file_id: int) -> StreamingResponse:
        file = self._get_file_or_raise(file_id)
        
    
            
        def iterfile():
            chunk_size = 1024 * 1024
            data = file.file_bytes
            
            for i in range(0, len(data), chunk_size):
                yield data[i:i+chunk_size]
        
        encoded_name = urllib.parse.quote(file.file_name, safe='')
        
        headers = {
            "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_name}"
        }
        
        return StreamingResponse(
            iterfile(),
            media_type=file.content_type,
            headers=headers
        )
        
    def _get_file_or_raise(self, file_id: int) -> File:
        file = self.get_file(file_id)
        
        if not file:
            raise NoResultFound
        
        return file