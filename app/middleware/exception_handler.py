from fastapi import Request
from fastapi.responses import JSONResponse
from http import HTTPStatus

from app.exceptions.custom_exception import (
    BadRequest,
    ServiceError,
    UnauthorizedError
)


async def bad_request_exception_handler(
    request: Request,
    exc: BadRequest
):

    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        content={
            "success": False,
            "message": str(exc)
        }
    )


async def service_exception_handler(
    request: Request,
    exc: ServiceError
):

    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": str(exc)
        }
    )


async def unauthorized_exception_handler(
    request: Request,
    exc: UnauthorizedError
):

    return JSONResponse(
        status_code=HTTPStatus.UNAUTHORIZED,
        content={
            "success": False,
            "message": str(exc)
        }
    )