from fastapi import APIRouter, status
from app.core.config import settings

router = APIRouter(
    prefix="/health",
    tags=["Health Check"]
)

@router.get("", status_code=status.HTTP_200_OK)
async def health():
    return {"status": "maintenance" if settings.is_maintenance else "ok"}
