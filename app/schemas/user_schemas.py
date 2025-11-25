
from pydantic import BaseModel, EmailStr, ConfigDict, Field


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = Field(max_length=30)
    email: EmailStr = Field(max_length=30)
    password: str = Field(max_length=30)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = Field(max_length=30)
    email: EmailStr = Field(max_length=30)
    role: str = Field(max_length=30)


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = Field(max_length=30)
    email: EmailStr = Field(max_length=30)
    password: bytes
    role: str = Field(max_length=30)


class UserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str | None = Field(default=None, max_length=30)
    email: EmailStr | None = Field(default=None, max_length=30)
