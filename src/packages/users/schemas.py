from pydantic import BaseModel


class NewUser(BaseModel):
    username: str
    password: str
