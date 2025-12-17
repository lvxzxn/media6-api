from fastapi import APIRouter, Depends, status
from app.core.dependencies import get_current_user

from .schemas import CreateEventSchema
from .service import EventService

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

service = EventService()


@router.get(
    "",
    status_code=status.HTTP_200_OK,
)
async def list_events():
    return await service.list_events()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_event(
    payload: CreateEventSchema,
    user=Depends(get_current_user),
):
    event_id = await service.create_event(payload)
    return {
        "success": True,
        "id": event_id,
    }


@router.delete(
    "/{event_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_event(
    event_id: str,
    user=Depends(get_current_user),
):
    await service.delete_event(event_id)
    return {
        "success": True,
        "message": "Evento removido com sucesso",
    }
