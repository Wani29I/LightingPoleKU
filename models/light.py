from typing import Optional
from pydantic import BaseModel

class LightStatus(BaseModel):
    # poleId: Optional[str]
    status: int
