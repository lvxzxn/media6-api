from fastapi import APIRouter, HTTPException, Request
from .schemas import SendMailSchema
from .service import MailApplicationService

router = APIRouter(prefix="/mail", tags=["Mail"])
service = MailApplicationService()


@router.post("/send")
async def send_mail(payload: SendMailSchema, request: Request):
    client_ip = request.client.host if request.client else None

    try:
        await service.send_contact_email(payload, client_ip)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "success": True,
        "message": "Email enviado com sucesso"
    }
    