from typing import Optional
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class Download(BaseModel):
    id: str
    date: str
    file_url: str
    file_name: str
    anime: str
    episode_id: int
    title: str
    image_src: str
    progress: int
    total_size: int

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class Saved(BaseModel):
    anime_id: str
    name: str
    image_src: str
    week_day: Optional[str]

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )
