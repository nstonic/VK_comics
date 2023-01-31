import requests

from classes import Comic


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
