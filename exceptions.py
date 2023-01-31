from requests import Response
from requests.exceptions import RequestException


class VKAPIRequestError(RequestException):
    def __init__(self, error):
        self.error_code = error["error_code"]
        self.error_msg = error["error_msg"]
        self.method = next(filter(lambda param: param["key"] == "method", error["request_params"]))

    def __str__(self):
        return f"\nError code: {self.error_code}\nMethod: {self.method['value']}\n{self.error_msg}"


def check_response_for_error(response: Response):
    response.raise_for_status()
    try:
        error = response.json()["error"]
    except KeyError:
        return
    raise VKAPIRequestError(error)
