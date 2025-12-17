from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from fastapi import HTTPException, status

from app.core.config import settings
import jwt

JWT_ALGORITHM = "HS256"
JWT_EXPIRES_IN_HOURS = 24

def create_jwt(payload: Dict[str, Any]) -> str:
    now = datetime.now(timezone.utc)

    to_encode = {
        **payload,
        "iat": now,
        "exp": now + timedelta(hours=JWT_EXPIRES_IN_HOURS),
    }

    token = jwt.encode(
        to_encode,
        settings.media6_password,
        algorithm=JWT_ALGORITHM,
    )

    return token


def decode_jwt(token: str) -> Dict[str, Any]:
    try:
        decoded = jwt.decode(
            token,
            settings.media6_password,
            algorithms=[JWT_ALGORITHM],
        )
        return decoded

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )
