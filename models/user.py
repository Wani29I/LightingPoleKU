from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class SuperUser(BaseModel):
    username: str
    password: str
