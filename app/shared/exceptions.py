class AppException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class UnauthorizedException(AppException):
    """Usuário não autenticado ou token inválido."""
    pass


class NotFoundException(AppException):
    """Recurso não encontrado."""
    pass


class ValidationException(AppException):
    """Erro de validação de regra de negócio."""
    pass


class ExternalServiceException(AppException):
    """Erro em serviços externos (mail, hCaptcha)."""
    pass