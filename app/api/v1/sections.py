from fastapi import Depends, status, Query
from fastapi.routing import APIRouter
from typing import Optional
from sqlalchemy.orm import Session

from ...service.section_service import SectionService
from ...database import get_db
from ...models.course import CourseSection
from ...schemas.course import SectionCreate, SectionUpdate, SectionResponse


router = APIRouter(prefix="/sections", tags=["Sections"])

def get_section_service(session: Session = Depends(get_db)) -> SectionService:
    return SectionService(session)


@router.get("/", response_model=list[SectionResponse])
def list_sections(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=0, le=1000),
    section_service: SectionService = Depends(get_section_service)
) -> list[CourseSection]:
    return section_service.list_sections(skip, limit)


@router.get("/{section_id}", response_model=SectionResponse)
def get_section(
    section_id: int,
    section_service: SectionService = Depends(get_section_service)
) -> Optional[CourseSection]:
    return section_service.get_section(section_id)


@router.post("/", response_model=SectionResponse)
def create_section(
    section_data: SectionCreate,
    section_service: SectionService = Depends(get_section_service)
) -> CourseSection:
    return section_service.create_section(section_data)


@router.put("/{section_id}", response_model=SectionResponse)
def update_section(
    section_id: int,
    section_data: SectionUpdate,
    section_service: SectionService = Depends(get_section_service)
) -> CourseSection:
    return section_service.update_section(section_id, section_data)


@router.delete("/{section_id}",
    status_code=status.HTTP_204_NO_CONTENT
    )
def delete_section(
    section_id: int,
    section_service: SectionService = Depends(get_section_service)
):
    section_service.delete_section(section_id)