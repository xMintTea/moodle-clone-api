from fastapi import Depends, status, Query, Path
from fastapi.routing import APIRouter
from typing import Optional

from ...models.course import Resource
from ...schemas.resources import ResourceResponse
from ...resources.resources import (
    get_resources_dependency,
    get_resouce_dependency,
    create_resource_dependency,
    update_resource_dependency
)


router = APIRouter(prefix="/resources", tags=["Resources"])


@router.get("/", response_model=list[ResourceResponse])
def get_Resources(
    Resources: list[Resource] = Depends(get_resources_dependency())
) -> list[Resource]:
    return Resources

@router.get("/{resource_id}", response_model=ResourceResponse)
def get_Resource(
    resource: Resource = Depends(get_resouce_dependency())
) -> Optional[Resource]:
    return resource

@router.post("/", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
def create_Resource(
    resource: Resource = Depends(create_resource_dependency())
) -> Resource:
    return resource

@router.put("/{Resource_id}", response_model=ResourceResponse, status_code=status.HTTP_202_ACCEPTED)
def update_Resource(
    resource: Resource = Depends(update_resource_dependency())
) -> Resource:
    return resource


