from app.core.config import settings
from app.core.security import create_jwt
from app.shared.exceptions import UnauthorizedException


class AuthService:
    def authenticate(self, password: str) -> str:
        if password != settings.media6_password:
            raise UnauthorizedException("Senha inválida")

        token = create_jwt({})
        return token
