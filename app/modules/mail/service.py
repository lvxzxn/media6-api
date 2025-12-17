from app.mailer import MailService
from app.core.config import settings
from .schemas import SendMailSchema
from .hcaptcha import verify_hcaptcha

class MailApplicationService:
    def __init__(self):
        self.mailer = MailService()

    async def send_contact_email(
        self,
        payload: SendMailSchema,
        client_ip: str | None,
    ) -> None:
        captcha_valid = await verify_hcaptcha(
            token=payload.hcaptcha_token,
            remoteip=client_ip
        )

        if not captcha_valid:
            raise ValueError("hCaptcha inválido")

        success = self.mailer.send_proposal(
            to_email=settings.from_email,
            user_name=payload.name,
            user_contact=payload.contact,
            user_message=payload.message,
        )
        
        if not success:
            raise RuntimeError("Falha ao enviar email")