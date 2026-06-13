from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from datetime import datetime
from typing import Optional
from fastapi import UploadFile
from fastapi.responses import StreamingResponse
import urllib.parse

from ..models.user import StudentGroup
from ..schemas.groups import GroupCreate, GroupUpdate


class GroupService:
    def __init__(self, session: Session) -> None:
        self._db = session
    
    
    def create_group(self, group_data: GroupCreate) -> StudentGroup:
        
        group = StudentGroup(**group_data.model_dump())
        
        self._db.add(group)
        self._db.commit()
        self._db.refresh(group)
        
        return group
    
    
    def get_group(self, group_id: int) -> Optional[StudentGroup]:
        return self._db.get(StudentGroup, group_id)
    
    
    def update_group(self, group_id: int, group_data: GroupUpdate) -> StudentGroup:
        group = self._get_group_or_raise(group_id)
        
        update_dict = group_data.model_dump(exclude_none=True)
        
        for field, value in update_dict.items():
            setattr(group, field, value)
        
        self._db.commit()
        self._db.refresh(group)
        
        return group
    
        
    def _get_group_or_raise(self, group_id: int) -> StudentGroup:
        group = self.get_group(group_id)
        
        if not group:
            raise NoResultFound
        
        return group