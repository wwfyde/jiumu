from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(64), unique=True, index=True)
    hashed_password = Column(String(64))
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128), index=True)
    description = Column(String(512), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")


# class Call(Base):
#     __tablename__ = "calls"
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#
#     pass


class Intention(Base):
    __tablename__ = "intention"
    gid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    agent = Column(String(64), nullable=False, comment="坐席号")
    id = Column(Integer, unique=True, comment="意图号")
    name = Column(String(128), comment="意图名称")
    read_time = Column(DateTime, comment="读取时间")
    call_id = Column(String(64), comment="通话流水号")
    phone = Column(String(16), comment="手机号")


class Reminder(Base):

    __tablename__ = 'reminders'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    agent_id = Column(String(64), comment="坐席账号")
    call_id = Column(String(64), comment="通话ID")
    model_name = Column(String(64), comment="模型名称")
    reminder_name = Column(String(64), comment="提醒名称")
    reminder_id = Column(String(64), comment="提醒ID")
    type = Column(Integer, comment="提醒类型")
    color = Column(String(16), comment="背景颜色")
    time = Column(DateTime, nullable=False, comment="提醒时间")
    call_time = Column(DateTime, comment="来电时间")
    phone = Column(String(16), comment="客户手机号")

    ring_time = Column(DateTime, comment="响铃时间")
    agent_account = Column(String(32), comment="坐席分析系统账号")
    direction = Column(String(8), comment="呼叫方向")
    total_time = Column(Integer, comment="通话时长")
    caller = Column(String(16), comment="主叫号码")
    called = Column(String(16), comment="被叫号码")
    hit_word = Column(String(64), comment="命中模型内容")
    keyword_type = Column(String(64), comment="命中关键词类型")
    keyword = Column(String(64), comment="命中关键词")


class Question(Base):
    """
    问题点击次数
    """
    pass
    __tablename__ = "questions"
    question = Column(String(64), primary_key=True, unique=True, comment="问题名称")

    access_times = Column(Integer, comment="访问次数")


class Feedback(Base):
    """
    问题反馈统计
    """

    __tablename__ = "feedbacks"
    question = Column(String(64), primary_key=True, comment="问题名称")
    knowledge_id = Column(Integer, unique=True, comment="问题ID")
    feedback = Column(Integer, default=0, nullable=False, comment="反馈结果")
    agent = Column(String(64), comment="坐席账号")


class Demo(Base):
    __tablename__ = "demo"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False, unique=True)
    type = Column(Boolean(), default=True)
    date = Column(DateTime, )
    desc = Column(String(64))


