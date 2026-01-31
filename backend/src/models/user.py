from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    name: str
    is_verified: bool = Field(default=False)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class UserUpdate(SQLModel):
    email: Optional[str] = None
    is_verified: Optional[bool] = None