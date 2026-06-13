from fastapi import APIRouter, Depends

from ...security.authorization import bearer_scheme
from .users import router as users_router
from .courses import router as courses_router
from .sections import router as sections_router
from .pages import router as pages_router
from .tests import router as tests_router
from .files import router as files_router
from .auth import router as auth_router
from .resources import router as resources_router
from .videos import router as video_router
from .groups import router as group_router

router = APIRouter(prefix="/v1",  dependencies=[Depends(bearer_scheme)])

router.include_router(auth_router)
router.include_router(group_router)
router.include_router(users_router)
router.include_router(courses_router)
router.include_router(sections_router)
router.include_router(pages_router)
router.include_router(tests_router)
router.include_router(resources_router)
router.include_router(video_router)
router.include_router(files_router)