import os
from random import randint

import requests
from dotenv import load_dotenv

from classes import Comic
from classes import Environs
from classes import SavedImage
from classes import UploadedImage
from comics import get_last_comic_number
from comics import get_comic_by_id
from exceptions import check_response_for_error


def get_wall_upload_server(environs: Environs) -> str:
    url = "https://api.vk.com/method/photos.getWallUploadServer"
    params = {
        "access_token": environs.access_token,
        "group_id": environs.group_id,
        "v": "5.124"
    }
    response = requests.get(url, params=params)
    check_response_for_error(response)
    return response.json()["response"]["upload_url"]


def load_photo_to_server(comic: Comic, environs: Environs) -> UploadedImage:
    upload_server = get_wall_upload_server(environs=environs)
    comic.download_comic_image()
    with open(comic.image_file_name, "rb") as file:
        response = requests.post(
            upload_server,
            files={"file1": file}
        )
    check_response_for_error(response)
    return UploadedImage.parse_raw(response.text)


def save_wall_photo(uploaded_image: UploadedImage,
                    environs: Environs) -> SavedImage:
    url = "https://api.vk.com/method/photos.saveWallPhoto"
    params = {
        "access_token": environs.access_token,
        "user_id": environs.user_id,
        "group_id": environs.group_id,
        "hash": uploaded_image.hash,
        "photo": uploaded_image.photo,
        "server": uploaded_image.server,
        "v": "5.124"
    }
    response = requests.get(url, params=params)
    check_response_for_error(response)
    return SavedImage.parse_obj(response.json()["response"][0])


def post_on_wall(comic: Comic, environs: Environs):
    url = "https://api.vk.com/method/wall.post"
    uploaded_image = load_photo_to_server(
        comic=comic,
        environs=environs
    )
    saved_image = save_wall_photo(
        uploaded_image=uploaded_image,
        environs=environs
    )

    params = {
        "access_token": environs.access_token,
        "v": "5.124",
        "owner_id": -environs.group_id,
        "from_group": 1,
        "signed": 1,
        "attachments": f"photo{saved_image.owner_id}_{saved_image.media_id}",
        "message": comic.alt,
        "hash": uploaded_image.hash,
        "photo": uploaded_image.photo,
        "server": uploaded_image.server
    }
    response = requests.post(url, params=params)
    check_response_for_error(response)


def main():
    load_dotenv()
    environs = Environs(
        access_token=os.environ["ACCESS_TOKEN"],
        group_id=int(os.environ["GROUP_ID"]),
        user_id=int(os.environ["USER_ID"])
    )
    comic = get_comic_by_id(
        randint(
            1,
            get_last_comic_number()
        )
    )
    try:
        post_on_wall(comic, environs)
    finally:
        if comic.image_file_name:
            os.remove(comic.image_file_name)


if __name__ == "__main__":
    main()
