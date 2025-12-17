from typing import List
from datetime import datetime, timezone
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class EventRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection = db.event

    async def find_upcoming(self) -> List[dict]:
        now = datetime.now(timezone.utc)

        events = await self._collection.find(
            {"date": {"$gte": now}}
        ).sort("date", 1).to_list(length=1000)

        return events

    async def create(self, data: dict) -> ObjectId:
        result = await self._collection.insert_one(data)
        return result.inserted_id

    async def delete_by_id(self, event_id: ObjectId) -> bool:
        result = await self._collection.delete_one({"_id": event_id})
        return result.deleted_count == 1
