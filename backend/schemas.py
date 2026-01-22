from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

class UserBase(BaseModel):
    fullName: str
    email: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(UserBase):
    id: int
    createdOn: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    accessToken: str
    user: UserResponse
    message: str

class TravelStoryBase(BaseModel):
    title: str
    story: str
    visitedLocation: List[str]
    imageUrl: str
    visitedDate: datetime

class TravelStoryCreate(TravelStoryBase):
    pass

class TravelStoryUpdate(BaseModel):
    title: Optional[str] = None
    story: Optional[str] = None
    visitedLocation: Optional[List[str]] = None
    imageUrl: Optional[str] = None
    visitedDate: Optional[datetime] = None

class TravelStoryResponse(TravelStoryBase):
    id: int
    userId: int
    isFavourite: bool
    createdOn: datetime

    class Config:
        from_attributes = True
