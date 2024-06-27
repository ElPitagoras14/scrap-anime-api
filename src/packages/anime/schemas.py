from pydantic import BaseModel


class Download(BaseModel):
    id: str
    date: str
    file_url: str
    file_name: str
    anime: str
    episode_id: int
    description: str
    image_src: str
    progress: int
    total_size: int
