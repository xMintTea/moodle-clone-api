from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from datetime import datetime
from typing import Optional

from ..models.course import Resource
from ..models.file import File
from ..schemas.resources import ResourceCreate, ResourceUpdate
from ..schemas.submission import PageSubmissionCreate, PageSubmissionUpdate


class ResourceService:
    def __init__(self, session: Session) -> None:
        self._db = session
    
    
    def list_resources(self, skip: int = 0, limit: int = 100) -> list[Resource]:
        stmt = select(Resource).offset(skip).limit(limit)
        return list(self._db.scalars(stmt).all())
    
    def get_resource(self, resource_id: int) -> Optional[Resource]:
        return self._db.get(Resource, resource_id)
    
    def create_resource(self, resource_data: ResourceCreate) -> Resource:
        resource = Resource(**resource_data.model_dump())
        self._db.add(resource)
        self._db.commit()
        self._db.refresh(resource)
        
        return resource
    
    def update_resource(self,resource_id: int, resource_data: ResourceUpdate) -> Resource:
        resource = self._get_resource_or_raise(resource_id)
        
        update_dict = resource_data.model_dump(exclude_unset=True)
        
        for field, value in update_dict.items():
            setattr(resource, field, value)
        
        self._db.commit()
        self._db.refresh(resource)
        
        return resource
    
    
    def _get_resource_or_raise(self, resource_id) -> Resource:
        resource = self.get_resource(resource_id)
        if resource is None:
            raise NoResultFound()
        return resource