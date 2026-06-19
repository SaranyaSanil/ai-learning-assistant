from fastapi import Request
from fastapi.responses import JSONResponse
from http import HTTPStatus

from app.exceptions.custom_exception import (
    BadRequest,
    ServiceError,
    UnauthorizedError,
    ResourceNotFoundError
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

async def resource_not_found_exception_handler(
    request: Request,
    exc: ResourceNotFoundError
):

    return JSONResponse(
        status_code=HTTPStatus.NOT_FOUND,
        content={
            "success": False,
            "message": str(exc)
        }
    )

async def expired_signature_exception_handler(
    request: Request,
    exc: Exception
):

    return JSONResponse(
        status_code=HTTPStatus.UNAUTHORIZED,
        content={
            "success": False,
            "message": "Token has expired"
        }
    )

async def invalid_token_exception_handler(
    request: Request,
    exc: Exception
):

    return JSONResponse(
        status_code=HTTPStatus.UNAUTHORIZED,
        content={
            "success": False,
            "message": "Invalid token"
        }
    )