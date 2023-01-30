import os
from random import randint

from dotenv import load_dotenv
import requests

from classes import Comic, WallUploadServer, UploadedImage, SavedImage, Environs
from comics import get_comic_image, get_comic_by_id, get_last_comic_number


def get_wall_upload_server(environs: Environs) -> WallUploadServer:
    url = "https://api.vk.com/method/photos.getWallUploadServer"
    params = {
        "access_token": environs.access_token,
        "group_id": environs.group_id,
        "v": "5.124"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return WallUploadServer.parse_obj(response.json()['response'])


def load_photo_to_server(comic: Comic, environs: Environs) -> UploadedImage:
    upload_server = get_wall_upload_server(environs)

    image_file_name = get_comic_image(comic)
    with open(image_file_name, "rb") as file:
        response = requests.post(upload_server.upload_url, files={"file1": file})
    os.remove(image_file_name)
    response.raise_for_status()
    return UploadedImage.parse_raw(response.text)


def save_wall_photo(uploaded_image: UploadedImage, environs: Environs) -> SavedImage:
    url = "https://api.vk.com/method/photos.saveWallPhoto"
    params = {
        "access_token": environs.access_token,
        "user_id": environs.user_id,
        "group_id": environs.group_id,
        'hash': uploaded_image.hash,
        'photo': uploaded_image.photo,
        'server': uploaded_image.server,
        "v": "5.124"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return SavedImage.parse_obj(response.json()["response"][0])


def post_on_wall(comic: Comic, environs: Environs):
    uploaded_image = load_photo_to_server(comic, environs)
    saved_image = save_wall_photo(uploaded_image, environs)

    url = "https://api.vk.com/method/wall.post"
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
    requests.post(url, params=params)


def main():
    load_dotenv()
    environs = Environs(
        access_token=os.environ["ACCESS_TOKEN"],
        group_id=int(os.environ["GROUP_ID"]),
        user_id=int(os.environ["USER_ID"])
    )
    comic = get_comic_by_id(randint(1, get_last_comic_number()))
    post_on_wall(comic, environs)


if __name__ == '__main__':
    main()
