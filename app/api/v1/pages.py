from fastapi import Depends, status, Query
from fastapi.routing import APIRouter
from typing import Optional
from sqlalchemy.orm import Session

from ...service.page_service import PageService
from ...database import get_db
from ...models.course import SectionPage
from ...schemas.course import PageCreate, PageUpdate, PageResponse


router = APIRouter(prefix="/pages", tags=["Pages"])

def get_page_service(session: Session = Depends(get_db)) -> PageService:
    return PageService(session)

@router.get("/{section_id}", response_model=list[PageResponse])
def list_pages(
    section_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=0, le=1000),
    page_service: PageService = Depends(get_page_service)
) -> list[SectionPage]:
    return page_service.list_pages(section_id, skip, limit)


@router.get("/page/{page_id}", response_model=PageResponse)
def get_page(
    page_id: int,
    page_service: PageService = Depends(get_page_service)
) -> Optional[SectionPage]:
    return page_service.get_page(page_id)


@router.post("/", response_model=PageResponse)
def create_page(
    page_data: PageCreate,
    page_service: PageService = Depends(get_page_service)
) -> SectionPage:
    return page_service.create_page(page_data)

@router.put("/{page_id}", response_model=PageResponse)
def update_page(
    page_id: int,
    page_data: PageUpdate,
    page_service: PageService = Depends(get_page_service)
) -> SectionPage:
    return page_service.update_page(page_id, page_data)

@router.delete("/{page_id}",
    status_code=status.HTTP_204_NO_CONTENT
    )
def delete_page(
    page_id: int,
    page_service: PageService = Depends(get_page_service)
):
    page_service.delete_page(page_id)