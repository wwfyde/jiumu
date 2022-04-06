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
    knowledge_id: Optional[int] = None
    feedback: int
    call_id: str
    agent: Union[int, str]


class CallQuestion(BaseModel):
    question: str
    knowledge_id: Optional[int] = None
    intention: Optional[int] = None
    call_id: str
    agent_id: Union[int, str]
    intention_name: Optional[str] = None
    source: Optional[int] = 2


class Question(BaseModel):
    id: int
    name: str


class QuestionCreate(Question):
    create_time: Optional[str] = None
    update_time: Optional[str] = None


class QuestionFeedback(Question):
    feedback: int = 0


class QuestionStatistics(Question):
    access_times: Optional[int] = None


