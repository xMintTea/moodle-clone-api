from fastapi import Depends, status, Query, Path
from fastapi.routing import APIRouter
from typing import Optional

from ...models.course import Test
from ...schemas.tests import TestResponse
from ...schemas.test_answers import AnswerBase, AnswerResponse
from ...schemas.questions import Question
from ...resources.tests import (
    list_tests_dependency,
    get_test_dependency,
    create_test_dependency,
    update_test_dependency,
    delete_test_dependency,
    get_attempts_dependency,
    create_attempt_dependency,
    get_user_tests_attempts_dependency
)


router = APIRouter(prefix="/tests", tags=["Tests"])


@router.get("/", response_model=list[TestResponse])
def list_tests(
    tests: list[Test]= Depends(list_tests_dependency())
) -> list[Test]:
    return tests


@router.get("/{test_id}", response_model=TestResponse)
def get_test(
    test: Optional[Test] = Depends(get_test_dependency())
) -> Optional[Test]:
    return test


@router.post("/", response_model=TestResponse, status_code=status.HTTP_201_CREATED)
def create_test(
    test: Test = Depends(create_test_dependency())
) -> Test:
    return test


@router.put("/{test_id}", response_model=TestResponse, status_code=status.HTTP_202_ACCEPTED)
def update_test(
    test: Test = Depends(update_test_dependency())
) -> Test:
    return test


@router.delete("/{test_id}",
    status_code=status.HTTP_204_NO_CONTENT
    )
def delete_test(
    _ = Depends(delete_test_dependency())
):
    ...

@router.get("/{test_id}/attempts", response_model=list[AnswerResponse])
def get_attempts(
    attemps = Depends(get_attempts_dependency())
):
    return attemps


@router.post("/{test_id}/attempts")
def create_attempt(
    attempt = Depends(create_attempt_dependency())
):
    return attempt


@router.get("/attempts/{user_id}")
def get_user_tests_attempts(
    attempts = Depends(get_user_tests_attempts_dependency())
):
    return attempts