from fastapi import Depends, status, Query, Path
from fastapi.routing import APIRouter
from typing import Optional, Annotated
from sqlalchemy.orm import Session

from ...service.section_service import SectionService
from ...database import get_db
from ...models.course import CourseSection, Test, SectionPage
from ...schemas.sections import SectionCreate, SectionUpdate, SectionResponse
from ...schemas.tests import TestResponse
from ...schemas.pages import PageResponse


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
    section_id: Annotated[int, Path(ge=1)],
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
    section_id: Annotated[int, Path(ge=1)],
    section_data: SectionUpdate,
    section_service: SectionService = Depends(get_section_service)
) -> CourseSection:
    return section_service.update_section(section_id, section_data)


@router.delete("/{section_id}",
    status_code=status.HTTP_204_NO_CONTENT
    )
def delete_section(
    section_id: Annotated[int, Path(ge=1)],
    section_service: SectionService = Depends(get_section_service)
):
    section_service.delete_section(section_id)
    
    
@router.get("/{section_id}/pages/", response_model=list[PageResponse])
def get_pages_in_section(
    section_id: Annotated[int, Path(ge=1)],
    section_service: SectionService = Depends(get_section_service)
) -> list[SectionPage]:
    return section_service.get_pages(section_id)


@router.get("/{section_id}/tests/", response_model=list[TestResponse])
def get_tests_in_section(
    section_id: Annotated[int, Path(ge=1)],
    section_service: SectionService = Depends(get_section_service)
) -> list[Test]:
    return section_service.get_tests(section_id)

