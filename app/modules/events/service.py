from bson import ObjectId
from datetime import timezone

from app.db.mongo import db
from app.shared.exceptions import (
    ValidationException,
    NotFoundException,
)
from app.shared.utils import serialize_mongo_document
from .repository import EventRepository

class EventService:
    def __init__(self):
        self.repo = EventRepository(db)

    async def list_events(self):
        events = await self.repo.find_upcoming()
        return [serialize_mongo_document(event) for event in events]

    async def create_event(self, event):
        data = event.dict()
        data["date"] = data["date"].astimezone(timezone.utc)

        event_id = await self.repo.create(data)
        return str(event_id)

    async def delete_event(self, event_id: str):
        try:
            oid = ObjectId(event_id)
        except Exception:
            raise ValidationException("ID de evento inválido")

        deleted = await self.repo.delete_by_id(oid)
        if not deleted:
            raise NotFoundException("Evento não encontrado")