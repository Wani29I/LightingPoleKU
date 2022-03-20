from datetime import datetime
from typing import Optional
from pydantic import BaseModel
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    permission: Optional[int] = 0

class UserInDB(User):
    hashed_password: str

class NewUser(User):
    password: str
