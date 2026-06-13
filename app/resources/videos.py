from fastapi import Depends, status, Query, Path
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from typing import Optional, Annotated
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..models.course import Video
from ..service.video_service import VideoService
from ..security.authorization import get_verified_user
from ..schemas.videos import VideoCreate, VideoUpdate


def get_video_service(session: Session = Depends(get_db)):
    return VideoService(session)



def get_videos_dependency():
    def dependency(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        course_id: int = Query(None, ge=1),
        video_service: VideoService = Depends(get_video_service),
        user: User = Depends(get_verified_user)
    ) -> list[Video]:
        return video_service.list_videos(skip, limit, course_id)
     
    return dependency


def get_video_dependency():
    def dependency(
        video_id: Annotated[int, Path(...,ge=1)],
        video_service: VideoService = Depends(get_video_service),
        user: User = Depends(get_verified_user)
    ) -> Optional[Video]:
        return video_service.get_video(video_id)
    
    return dependency


def create_video_dependency():
    def dependency(
        video_data: VideoCreate,
        video_service: VideoService = Depends(get_video_service),
        user: User = Depends(get_verified_user)
    ) -> Video:
        return video_service.create_video(video_data)
    
    return dependency


def update_video_dependency():
    def dependency(
        video_id: Annotated[int, Path(...,ge=1)],
        video_data: VideoUpdate,
        video_service: VideoService = Depends(get_video_service),
        user: User = Depends(get_verified_user)
    ) -> Video:
        return video_service.update_video(video_id, video_data)
    
    return dependency