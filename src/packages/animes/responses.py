from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from utils.responses import SuccessResponse


class Link(BaseModel):
    service: str
    link: str


class AnimeDownloadLink(BaseModel):
    name: str
    download_info: Link | None
    episode_id: int

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class AnimeDownloadLinkList(BaseModel):
    name: str
    episodes: list[AnimeDownloadLink | None] | None
    total: int


class Episode(BaseModel):
    name: str
    link: str
    episode_id: int

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class AnimeStreamingLinks(BaseModel):
    name: str
    episodes: list[Episode] | None
    total: int


class AnimeStreamingLinksOut(SuccessResponse):
    payload: AnimeStreamingLinks | None


class AnimeDownloadLinkOut(SuccessResponse):
    payload: AnimeDownloadLink | None


class AnimeDownloadLinkListOut(SuccessResponse):
    payload: AnimeDownloadLinkList | None


class Anime(BaseModel):
    anime_id: str
    name: str
    description: str
    image_src: str
    is_finished: bool
    week_day: str | None
    is_saved: bool = False

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class AnimeOut(SuccessResponse):
    payload: Anime | None


class AnimeList(BaseModel):
    items: list[Anime]
    total: int


class AnimeListOut(SuccessResponse):
    payload: AnimeList | None


class AnimeCard(BaseModel):
    name: str
    image_src: str
    anime_id: str
    is_saved: bool = False

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class AnimeCardList(BaseModel):
    items: list[AnimeCard]
    total: int


class AnimeCardListOut(SuccessResponse):
    payload: AnimeCardList | None
