from fastapi import APIRouter
from .user import user_router

main_router = APIRouter(prefix="/app")

main_router.include_router(router=user_router, tags=["Users"])
