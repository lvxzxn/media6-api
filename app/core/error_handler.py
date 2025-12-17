from fastapi import Request
from fastapi.responses import JSONResponse

from app.shared.exceptions import AppException


async def app_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    if isinstance(exc, AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.message,
            },
        )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Erro interno inesperado",
        },
    )
