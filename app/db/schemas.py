from typing import List, Optional, Union

from pydantic import BaseModel
from sqlalchemy import DateTime


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True


class Demo(BaseModel):
    name: str
    type: bool
    desc: str

# class


class Feedback(BaseModel):
    question: str
    knowledge_id: int
    feedback: int
    agent: Union[int, str]


class Question(BaseModel):
    question: str
    knowledge_id: int
    intention: int
    agent: Union[int, str] | None = None


class QuestionCreate(Question):
    create_time: str | None = None
    update_time: str | None = None


class QuestionFeedback(Question):
    feedback: int = 0


class QuestionStatistics(Question):
    access_times: int | None = None


