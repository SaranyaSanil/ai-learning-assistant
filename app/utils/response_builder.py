from typing import Any


class ResponseBuilder:

    @staticmethod
    def success(
        data: Any = None,
        message: str = "Success",
        status_code: int = 200
    ):

        return {
            "success": True,
            "message": message,
            "data": data,
            "status_code": status_code
        }

    @staticmethod
    def error(
        message: str = "Something went wrong",
        status_code: int = 400
    ):

        return {
            "success": False,
            "message": message,
            "status_code": status_code
        }