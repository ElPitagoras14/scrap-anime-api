from pydantic import BaseModel


class Anime(BaseModel):
    title: str


class Episode(BaseModel):
    episodeLink: str
