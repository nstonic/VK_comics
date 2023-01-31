import os
from urllib.parse import unquote, urlparse
from typing import NamedTuple

import requests
from pydantic import BaseModel, Field


class Comic(BaseModel):
    num: int
    safe_title: str
    alt: str
    image_url: str = Field(alias="img")
    image_file_name: str = None

    def _get_image_file_name(self):
        parsed_link = unquote(urlparse(self.image_url).path)
        ext = os.path.splitext(parsed_link)[1]
        self.image_file_name = f"{self.safe_title}{ext}"

    def download_comic_image(self):
        response = requests.get(self.image_url)
        response.raise_for_status()
        self._get_image_file_name()
        with open(self.image_file_name, "wb") as img_file:
            img_file.write(response.content)


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


class Environs(NamedTuple):
    access_token: str
    group_id: int
    user_id: int
