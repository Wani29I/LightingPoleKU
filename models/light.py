from typing import Optional
from pydantic import BaseModel

class LightStatus(BaseModel):
    # poleId: Optional[str]
    status: int

class LightingPole(BaseModel):
  name: str
  lat: float
  long: float
  status: Optional[int] = 0

