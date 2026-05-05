from fastapi import Depends, status
from fastapi.routing import APIRouter
from typing import Optional

from ...models.course import SectionPage, SubmittedPage
from ...schemas.pages import PageResponse
from ...schemas.submission import PageSubmissionResponse
from ...resources.pages import (
    list_pages_dependency,
    get_page_dependency,
    create_page_dependency,
    update_page_dependency,
    delete_page_dependency,
    get_page_submissions_dependency,
    get_submission_dependency,
    create_page_submittion_dependency,
    add_file_to_the_page_dependency,
    add_file_to_the_submission_dependency
)


router = APIRouter(prefix="/pages", tags=["Pages"])


@router.get("/", response_model=list[PageResponse])
def list_pages(
    assignments: list[SectionPage] = Depends(list_pages_dependency())
) -> list[SectionPage]:
    return assignments


@router.get("/{page_id}", response_model=PageResponse)
def get_page(
    assignment: Optional[SectionPage] = Depends(get_page_dependency())
) -> Optional[SectionPage]:
    return assignment


@router.post("/", response_model=PageResponse, status_code=status.HTTP_201_CREATED)
def create_page(
    assignment: SectionPage = Depends(create_page_dependency())
) -> SectionPage:
    return assignment


@router.put("/{page_id}", response_model=PageResponse, status_code=status.HTTP_202_ACCEPTED)
def update_page(
    assignment: SectionPage = Depends(update_page_dependency())
) -> SectionPage:
    return assignment


@router.delete("/{page_id}",
    status_code=status.HTTP_204_NO_CONTENT
    )
def delete_page(
    _ = Depends(delete_page_dependency())
):
    ...


@router.get("/{page_id}/submittions/", response_model=list[PageSubmissionResponse])
def get_page_submittions(
    submissions: list[SubmittedPage] = Depends(get_page_submissions_dependency())
) -> list[SubmittedPage]:
    return submissions


@router.get("/submittions/{submittion_id}", response_model=PageSubmissionResponse)
def get_submittion(
    submission: Optional[SubmittedPage] = Depends(get_submission_dependency())
) -> Optional[SubmittedPage]:
    return submission


@router.post(
    "/{page_id}/submittions/",
    response_model=PageSubmissionResponse,
    status_code=status.HTTP_201_CREATED)
def create_page_submittion(
    submission: SubmittedPage = Depends(create_page_submittion_dependency())
) -> SubmittedPage:
    return submission


@router.put(
    "/submittions/{submittion_id}",
    response_model=PageSubmissionResponse,
    status_code=status.HTTP_202_ACCEPTED)
def update_page_submission(
    submission: SubmittedPage = Depends(update_page_dependency())
) -> SubmittedPage:
    return submission


@router.put(
    "/{page_id}/files/{file_id}",
    response_model=PageResponse,
    status_code=status.HTTP_202_ACCEPTED
)
def add_file_to_the_page(
    assignment: SectionPage = Depends(add_file_to_the_page_dependency())
) -> SectionPage:
    return assignment


@router.put(
    "/submittions/{submittion_id}/files/{file_id}",
    response_model=PageSubmissionResponse,
    status_code=status.HTTP_202_ACCEPTED
)
def add_file_to_the_submittion(
    submission: SubmittedPage = Depends(add_file_to_the_submission_dependency())
) -> SubmittedPage:
    return submission