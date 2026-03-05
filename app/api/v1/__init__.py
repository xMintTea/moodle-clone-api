from fastapi import APIRouter

from .users import router as users_router
from .courses import router as courses_router
from .sections import router as sections_router

router = APIRouter(prefix="/v1")

router.include_router(users_router)
router.include_router(courses_router)
router.include_router(sections_router)
