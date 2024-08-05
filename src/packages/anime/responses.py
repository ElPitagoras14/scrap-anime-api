from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from utils.responses import SuccessResponse

from .schemas import Saved


class DownloadLink(BaseModel):
    title: str
    link: str
    episode_id: int

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class AnimeDownloadLinks(BaseModel):
    name: str
    episodes: list[DownloadLink]
    total: int


class Episode(BaseModel):
    title: str
    link: str
    episode_id: int

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


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
    week_day: str | None

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class AnimeCard(BaseModel):
    name: str
    image_src: str
    anime_id: str

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


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


class SavedOut(SuccessResponse):
    payload: Saved | None


class SavedList(BaseModel):
    items: list[Saved]
    total: int


class SavedListOut(SuccessResponse):
    payload: SavedList | None
