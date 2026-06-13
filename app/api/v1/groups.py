from fastapi import Depends, status, Query, Path
from fastapi.routing import APIRouter
from typing import Optional

from ...models.user import StudentGroup
from ...schemas.groups import GroupResponse
from ...resources.groups import (
    get_group_dependency,
    create_group_dependency
)


router = APIRouter(prefix="/groups", tags=["Groups"])



@router.get("/{group_id}", response_model=GroupResponse)
def get_video(
    group: StudentGroup = Depends(get_group_dependency())
) -> Optional[StudentGroup]:
    return group

@router.post("/", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
def create_group(
    group: StudentGroup = Depends(create_group_dependency())
) -> StudentGroup:
    return group


