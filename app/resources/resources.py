from fastapi import Depends, status, Query, Path
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from typing import Optional, Annotated
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..models.course import Resource
from ..service.resource_service import ResourceService
from ..security.authorization import get_verified_user
from ..schemas.resources import ResourceCreate, ResourceUpdate


def get_resource_service(session: Session = Depends(get_db)):
    return ResourceService(session)



def get_resources_dependency():
    def dependency(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        resource_service: ResourceService = Depends(get_resource_service),
        user: User = Depends(get_verified_user)
    ) -> list[Resource]:
        return resource_service.list_resources(skip, limit)
    
    return dependency


def get_resouce_dependency():
    def dependency(
        resource_id: Annotated[int, Path(...,ge=1)],
        resource_service: ResourceService = Depends(get_resource_service),
        user: User = Depends(get_verified_user)
    ) -> Optional[Resource]:
        return resource_service.get_resource(resource_id)
    
    return dependency


def create_resource_dependency():
    def dependency(
        resource_data: ResourceCreate,
        resource_service: ResourceService = Depends(get_resource_service),
        user: User = Depends(get_verified_user)
    ) -> Resource:
        return resource_service.create_resource(resource_data)
    
    return dependency


def update_resource_dependency():
    def dependency(
        resource_id: Annotated[int, Path(...,ge=1)],
        resource_data: ResourceUpdate,
        resource_service: ResourceService = Depends(get_resource_service),
        user: User = Depends(get_verified_user)
    ) -> Resource:
        return resource_service.update_resource(resource_id, resource_data)
    
    return dependency