from typing import Optional
from pydantic import BaseModel

class Event(BaseModel):
    headUserId: str
    countUserJoin: int
    dateTime: str
    place: str
    eventName: str
    description: str
class User(BaseModel):
    name: str
    age: int
    event: Optional[list[Event]]


    