from pydantic import BaseModel

from utils.responses import SuccessResponse

from .schemas import Download


class DownloadLink(BaseModel):
    name: str
    link: str
    episode_id: int


class AnimeDownloadLinks(BaseModel):
    name: str
    episodes: list[DownloadLink]
    total: int


class Episode(BaseModel):
    name: str
    link: str
    episode_id: int


class AnimeLinks(BaseModel):
    name: str
    episodes: list[Episode] | None
    total: int


class AnimeLinksOut(SuccessResponse):
    payload: AnimeLinks | None


class Anime(BaseModel):
    name: str
    finished: bool
    description: str
    image_src: str


class AnimeCard(BaseModel):
    title: str
    image_src: str
    anime_id: str


class AnimeCardList(BaseModel):
    items: list[AnimeCard]
    total: int


class DownloadLinkOut(SuccessResponse):
    payload: DownloadLink | None


class AnimeDownloadLinksOut(SuccessResponse):
    payload: AnimeDownloadLinks | None


class AnimeOut(SuccessResponse):
    payload: Anime | None


class AnimeCardListOut(SuccessResponse):
    payload: AnimeCardList | None


class DownloadHistoryOut(SuccessResponse):
    payload: list[Download] | None
