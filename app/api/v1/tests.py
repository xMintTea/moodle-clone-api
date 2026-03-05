from fastapi import Depends, status, Query
from fastapi.routing import APIRouter
from typing import Optional
from sqlalchemy.orm import Session

from ...service.test_service import TestService
from ...database import get_db
from ...models.course import Test
from ...schemas.course import TestCreate, TestUpdate, TestResponse


router = APIRouter(prefix="/tests", tags=["Tests"])


def get_test_service(session: Session = Depends(get_db)) -> TestService:
    return TestService(session)


@router.get("/{section_id}", response_model=list[TestResponse])
def list_tests(
    section_id: int,
    test_service: TestService = Depends(get_test_service)
) -> list[Test]:
    return test_service.list_tests(section_id)


@router.get("/test/{test_id}", response_model=TestResponse)
def get_test(
    test_id: int,
    test_service: TestService = Depends(get_test_service)
) -> Optional[Test]:
    return test_service.get_test(test_id)

@router.post("/", response_model=TestResponse)
def create_test(
    test_data: TestCreate,
    test_service: TestService = Depends(get_test_service)
) -> Test:
    return test_service.create_test(test_data)

@router.put("/{test_id}", response_model=TestResponse)
def update_test(
    test_id: int,
    test_data: TestUpdate,
    test_service: TestService = Depends(get_test_service)
) -> Test:
    return test_service.update_test(test_id, test_data)

@router.delete("/{test_id}",
    status_code=status.HTTP_204_NO_CONTENT
    )
def delete_test(
    test_id: int,
    test_service: TestService = Depends(get_test_service)
):
    test_service.delete_test(test_id)