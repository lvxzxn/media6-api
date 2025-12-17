from datetime import datetime
from pydantic import BaseModel, Field


class EventBaseSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=150)
    description: str = Field(..., min_length=10, max_length=5000)
    date: datetime
    location: str = Field(..., min_length=2, max_length=255)


class CreateEventSchema(EventBaseSchema):
    pass


class EventResponseSchema(EventBaseSchema):
    id: str

    class Config:
        from_attributes = True