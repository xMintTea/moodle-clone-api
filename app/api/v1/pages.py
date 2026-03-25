from fastapi import Depends, status, Query, Path
from fastapi.routing import APIRouter
from typing import Optional, Annotated
from sqlalchemy.orm import Session

from ...service.page_service import PageService
from ...database import get_db
from ...models.course import SectionPage, SubmittedPage
from ...schemas.pages import PageCreate, PageUpdate, PageResponse
from ...schemas.submission import PageSubmissionCreate, PageSubmissionResponse, PageSubmissionUpdate


router = APIRouter(prefix="/pages", tags=["Pages"])

def get_page_service(session: Session = Depends(get_db)) -> PageService:
    return PageService(session)

@router.get("/", response_model=list[PageResponse])
def list_pages(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=0, le=1000),
    page_service: PageService = Depends(get_page_service)
) -> list[SectionPage]:
    return page_service.list_pages(skip=skip, limit=limit)


@router.get("/{page_id}", response_model=PageResponse)
def get_page(
    page_id: Annotated[int, Path(ge=1)],
    page_service: PageService = Depends(get_page_service)
) -> Optional[SectionPage]:
    return page_service.get_page(page_id)


@router.post("/", response_model=PageResponse, status_code=status.HTTP_201_CREATED)
def create_page(
    page_data: PageCreate,
    page_service: PageService = Depends(get_page_service)
) -> SectionPage:
    return page_service.create_page(page_data)


@router.put("/{page_id}", response_model=PageResponse, status_code=status.HTTP_202_ACCEPTED)
def update_page(
    page_id: Annotated[int, Path(ge=1)],
    page_data: PageUpdate,
    page_service: PageService = Depends(get_page_service)
) -> SectionPage:
    return page_service.update_page(page_id, page_data)


@router.delete("/{page_id}",
    status_code=status.HTTP_204_NO_CONTENT
    )
def delete_page(
    page_id: Annotated[int, Path(ge=1)],
    page_service: PageService = Depends(get_page_service)
):
    page_service.delete_page(page_id)



@router.get("/{page_id}/submittions/", response_model=list[PageSubmissionResponse])
def get_page_submittions(
    page_id: Annotated[int, Path(ge=1)],
    user_id: Optional[int] = Query(None, ge=1),
    page_service: PageService = Depends(get_page_service)
) -> list[SubmittedPage]:
    return page_service.get_submittions(page_id, user_id)


@router.get("/submittions/{submittion_id}", response_model=PageSubmissionResponse)
def get_submittion(
    submittion_id: Annotated[int, Path(ge=1)],
    page_service: PageService = Depends(get_page_service)
) -> Optional[SubmittedPage]:
    return page_service.get_submittion(submittion_id)

@router.post(
    "/{page_id}/submittions/",
    response_model=PageSubmissionResponse,
    status_code=status.HTTP_201_CREATED)
def create_page_submittion(
    page_id: Annotated[int, Path(ge=1)],
    page_data: PageSubmissionCreate,
    page_service: PageService = Depends(get_page_service)
):
    return page_service.create_submittion(page_id, page_data)


@router.put(
    "/submittions/{submittion_id}",
    response_model=PageSubmissionResponse,
    status_code=status.HTTP_202_ACCEPTED)
def update_page_submission(
    submittion_id: Annotated[int, Path(ge=1)],
    submission_data: PageSubmissionUpdate,
    page_service: PageService = Depends(get_page_service)
) -> SubmittedPage:
    return page_service.update_submittion(submittion_id, submission_data)



@router.put(
    "/{page_id}/files/{file_id}",
    response_model=PageResponse,
    status_code=status.HTTP_202_ACCEPTED
)
def add_file_to_the_page(
    page_id: Annotated[int, Path(ge=1)],
    file_id: Annotated[int, Path(ge=1)],
    page_service: PageService = Depends(get_page_service)
) -> SectionPage:
    return page_service.add_file_to_page(page_id, file_id)

@router.put(
    "/submittions/{submittion_id}/files/{file_id}",
    response_model=PageSubmissionResponse,
    status_code=status.HTTP_202_ACCEPTED
)
def add_file_to_the_submittion(
    submittion_id: Annotated[int, Path(ge=1)],
    file_id: Annotated[int, Path(ge=1)],
    page_service: PageService = Depends(get_page_service)
) -> SubmittedPage:
    return page_service.add_file_to_submittion(submittion_id, file_id)


