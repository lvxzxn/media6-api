from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    media6_password: str

    jwt_secret: str
    hcaptcha_secret: str

    resend_api_key: str
    from_email: str = "contato@media6.com.br"
    from_name: str = "Media6"

    frontend_url: str = "http://localhost:3000"
    debug: bool = False
    env: str = "development"

    @property
    def is_prod(self) -> bool:
        return self.env.lower() == "production"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )


settings = Settings()  # type: ignore[call-arg]
