from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class RoutineBase(BaseModel):
    title: str
    description: Optional[str] = None
    date: date
    completed: bool = False

class RoutineCreate(RoutineBase):
    pass

class Routine(RoutineBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    routines: List[Routine] = []

    class Config:
        from_attributes = True
