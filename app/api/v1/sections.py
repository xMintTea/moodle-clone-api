from fastapi import Depends, status, Query, Path
from fastapi.routing import APIRouter
from typing import Optional

from ...models.course import CourseSection, Test, SectionPage
from ...schemas.sections import SectionResponse
from ...schemas.tests import TestResponse
from ...schemas.pages import PageResponse
from ...resources.sections import (
    list_section_dependency,
    get_section_dependency,
    create_section_dependency,
    update_section_dependency,
    delete_section_dependency,
    get_pages_in_section_dependency,
    get_tests_in_section_dependency
)


router = APIRouter(prefix="/sections", tags=["Sections"])


@router.get("/", response_model=list[SectionResponse])
def list_sections(
    sections: list[CourseSection] = Depends(list_section_dependency())
) -> list[CourseSection]:
    return sections


@router.get("/{section_id}", response_model=SectionResponse)
def get_section(
    section: Optional[CourseSection] = Depends(get_section_dependency())
) -> Optional[CourseSection]:
    return section


@router.post("/", response_model=SectionResponse)
def create_section(
    section: CourseSection = Depends(create_section_dependency())
) -> CourseSection:
    return section


@router.put("/{section_id}", response_model=SectionResponse)
def update_section(
    section: CourseSection = Depends(update_section_dependency())
) -> CourseSection:
    return section


@router.delete("/{section_id}",
    status_code=status.HTTP_204_NO_CONTENT
    )
def delete_section(
    _ = Depends(delete_section_dependency())
):
    ...


@router.get("/{section_id}/pages/", response_model=list[PageResponse])
def get_pages_in_section(
    assignments_in_section: list[SectionPage] = Depends(get_pages_in_section_dependency())
) -> list[SectionPage]:
    return assignments_in_section


@router.get("/{section_id}/tests/", response_model=list[TestResponse])
def get_tests_in_section(
    tests_in_section: list[Test] = Depends(get_tests_in_section_dependency())
) -> list[Test]:
    return tests_in_section