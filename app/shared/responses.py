from typing import Any, TypedDict, NotRequired


class SuccessResponse(TypedDict):
    success: bool
    message: NotRequired[str]
    data: NotRequired[Any]


class ErrorResponse(TypedDict):
    success: bool
    message: str
