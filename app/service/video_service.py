from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from datetime import datetime
from typing import Optional

from ..models.course import Video
from ..schemas.videos import VideoCreate, VideoUpdate
from ..schemas.submission import PageSubmissionCreate, PageSubmissionUpdate


class VideoService:
    def __init__(self, session: Session) -> None:
        self._db = session
    
    
    def list_videos(self, skip: int = 0, limit: int = 100, course_id: Optional[int] = None) -> list[Video]:
        stmt = select(Video).offset(skip).limit(limit)
        
        videos = list(self._db.scalars(stmt).all())
        
        if course_id is not None:
            videos = [i for i in videos if i.section.course_id == course_id]
        
        return videos
    
    def get_video(self, video_id: int) -> Optional[Video]:
        return self._db.get(Video, video_id)
    
    def create_video(self, video_data: VideoCreate) -> Video:
        video = Video(**video_data.model_dump())
        self._db.add(video)
        self._db.commit()
        self._db.refresh(video)
        
        return video
    
    def update_video(self,video_id: int, video_data: VideoUpdate) -> Video:
        video = self._get_video_or_raise(video_id)
        
        update_dict = video_data.model_dump(exclude_unset=True)
        
        for field, value in update_dict.items():
            setattr(video, field, value)
        
        self._db.commit()
        self._db.refresh(video)
        
        return video
    
    
    def _get_video_or_raise(self, video_id) -> Video:
        video = self.get_video(video_id)
        if video is None:
            raise NoResultFound()
        return video