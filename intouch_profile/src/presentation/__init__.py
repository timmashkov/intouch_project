from fastapi import APIRouter
from .profile import profile_router

main_router = APIRouter(prefix="/api")

main_router.include_router(router=profile_router, tags=["Profiles"])
