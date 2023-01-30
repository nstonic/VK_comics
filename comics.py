import os
from urllib.parse import unquote, urlparse

import requests

from classes import Comic


def _get_file_ext(url: str) -> str:
    parsed_link = unquote(urlparse(url).path)
    return os.path.splitext(parsed_link)[1]


def get_comic_image(comic: Comic) -> str:
    response = requests.get(comic.image_url)
    response.raise_for_status()
    image_file_name = f"{comic.safe_title}{_get_file_ext(comic.image_url)}"
    with open(image_file_name, "wb") as img_file:
        img_file.write(response.content)
    return image_file_name


def get_comic_by_id(comix_id: int) -> Comic:
    response = requests.get(f"https://xkcd.com/{comix_id}/info.0.json")
    response.raise_for_status()
    comic = Comic.parse_raw(response.text)
    return comic


def get_last_comic_number() -> int:
    response = requests.get("https://xkcd.com/info.0.json")
    response.raise_for_status()
    comic = Comic.parse_raw(response.text)
    return comic.num
