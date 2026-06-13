from fastapi import Depends, UploadFile, File as FileParam, Path
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from typing import Annotated, Optional
from sqlalchemy.exc import NoResultFound
from fastapi.responses import StreamingResponse

from ..database import get_db
from ..service.group_service import GroupService
from ..security.authorization import get_verified_user
from ..models.user import StudentGroup, User
from ..models.context.enums import UserType
from ..schemas.groups import GroupCreate, GroupUpdate



def get_group_service(session: Session = Depends(get_db)):
    return GroupService(session)


def create_group_dependency():
    def dependency(
        group_data: GroupCreate,
        user: User = Depends(get_verified_user),
        group_service: GroupService = Depends(get_group_service)
    ) -> StudentGroup:

        return group_service.create_group(group_data)
    
    return dependency


def get_group_dependency():
    def dependency(
        group_id: Annotated[int, Path(ge=1)],
        group_service: GroupService = Depends(get_group_service),
        user: User = Depends(get_verified_user)
    ) -> Optional[StudentGroup]:
        
        return group_service.get_group(group_id)
        

    
    return dependency
    
