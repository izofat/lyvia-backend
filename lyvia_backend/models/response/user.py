from datetime import datetime

from pydantic import BaseModel


class UserSuccessfullResponse(BaseModel):
    id: int
    username: str
    name: str
    lastName: str
    email: str
    jwtToken: str
    exp: datetime
