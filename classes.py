from dataclasses import dataclass

from pydantic import BaseModel, Field


class Comic(BaseModel):
    num: int
    safe_title: str
    alt: str
    image_url: str = Field(alias="img")


class WallUploadServer(BaseModel):
    upload_url: str
    album_id: int
    user_id: int


class UploadedImage(BaseModel):
    hash: str
    photo: str
    server: int


class SavedImage(BaseModel):
    media_id: int = Field(alias="id")
    owner_id: int


@dataclass
class Environs:
    access_token: str
    group_id: int
    user_id: int
