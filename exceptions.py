from requests import Response
from requests.exceptions import HTTPError


class VKAPIRequestError(HTTPError):
    def __init__(self, error: dict):
        self.error_code = error["error_code"]
        self.error_msg = error["error_msg"]
        self.method = (
            param["value"] for param
            in error["request_params"]
            if param["key"] == "method"
        )

    def __str__(self):
        return f"Error code: {self.error_code}" \
               f"\nMethod: {next(self.method)}" \
               f"\n{self.error_msg}"


def check_response_for_error(response: Response):
    response.raise_for_status()
    try:
        error = response.json()["error"]
    except KeyError:
        return
    raise VKAPIRequestError(error)
