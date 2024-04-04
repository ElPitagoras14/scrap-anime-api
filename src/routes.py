from fastapi import APIRouter

from packages.anime.router import anime_router


router = APIRouter()

router.include_router(anime_router, prefix="/anime", tags=["Anime"])
