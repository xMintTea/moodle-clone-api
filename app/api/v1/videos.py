from fastapi import Depends, status, Query, Path
from fastapi.routing import APIRouter
from typing import Optional

from ...models.course import Video
from ...schemas.videos import VideoResponse
from ...resources.videos import (
    get_videos_dependency,
    get_video_dependency,
    create_video_dependency,
    update_video_dependency
)


router = APIRouter(prefix="/videos", tags=["Videos"])


@router.get("/", response_model=list[VideoResponse])
def get_videos(
    videos: list[Video] = Depends(get_videos_dependency())
) -> list[Video]:
    return videos

@router.get("/{video_id}", response_model=VideoResponse)
def get_video(
    video: Video = Depends(get_video_dependency())
) -> Optional[Video]:
    return video

@router.post("/", response_model=VideoResponse, status_code=status.HTTP_201_CREATED)
def create_video(
    video: Video = Depends(create_video_dependency())
) -> Video:
    return video

@router.put("/{video_id}", response_model=VideoResponse, status_code=status.HTTP_202_ACCEPTED)
def update_video(
    video: Video = Depends(update_video_dependency())
) -> Video:
    return video


