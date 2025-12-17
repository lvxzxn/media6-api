from fastapi import Depends, HTTPException, Request, status
from app.core.security import decode_jwt

def get_current_user(request: Request):
    token = request.cookies.get("admin_cookie")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autenticado",
        )

    try:
        payload = decode_jwt(token)
        return payload
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
        )
