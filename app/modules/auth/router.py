from fastapi import APIRouter, Depends, Response, status

from .schemas import LoginSchema, AuthStatusResponse
from .service import AuthService
from app.core.dependencies import get_current_user

router = APIRouter(tags=["Auth"])
service = AuthService()


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(payload: LoginSchema, response: Response):
    token = service.authenticate(payload.password)

    response.set_cookie(
        key="admin_cookie",
        value=token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=60 * 60 * 24,
        path="/",
    )

    return {"success": True}


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response):
    response.delete_cookie("admin_cookie", path="/")
    return {"success": True}


@router.get("/auth-status", response_model=AuthStatusResponse)
async def auth_status(user=Depends(get_current_user)):
    return {"authenticated": True}