from datetime import datetime
from config import BaseModel


class CreateUser(BaseModel):
    username: str
    password: str


class GetUser(BaseModel):
    id: int
    username: str
    userspace: str
    storage_size: int
    created_at: datetime
