import datetime

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


class Intention(Base):
    __tablename__ = "intention"
    gid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # agent = Column(String(64), nullable=False, comment="坐席号")
    id = Column(Integer, unique=True, primary_key=True, nullable=False,
                comment="意图号")
    name = Column(String(128), comment="意图名称")
    # call_id = Column(String(64), comment="通话流水号")
    # phone = Column(String(16), comment="手机号")
    create_time = Column(DateTime, default=datetime.datetime.now(),
                         comment="创建时间")
    update_time = Column(DateTime, onupdate=datetime.datetime.now(),
                         comment="更新时间")


class Reminder(Base):
    __tablename__ = 'reminder'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    agent_id = Column(String(64), comment="坐席账号")
    agent_name = Column(String(64), comment="坐席姓名")
    call_id = Column(String(64), comment="通话ID")
    call_time = Column(DateTime, comment="来电时间")
    model_name = Column(String(64), comment="模型名称")
    reminder_name = Column(String(64), comment="提醒名称")
    reminder_id = Column(String(64), comment="提醒ID")
    type = Column(Integer, comment="提醒类型")
    color = Column(String(16), comment="背景颜色")
    time = Column(DateTime, nullable=False, comment="提醒时间")
    phone = Column(String(16), comment="客户手机号")
    create_time = Column(DateTime, default=datetime.datetime.now(),
                         comment="创建时间")
    update_time = Column(DateTime, onupdate=datetime.datetime.now(),
                         comment="更新时间")

    ring_time = Column(DateTime, comment="响铃时间")
    agent_account = Column(String(32), comment="坐席分析系统账号")
    direction = Column(String(8), comment="呼叫方向")
    total_time = Column(Integer, comment="通话时长")
    caller = Column(String(16), comment="主叫号码")
    called = Column(String(16), comment="被叫号码")
    hit_word = Column(String(64), comment="命中模型内容")
    keyword_type = Column(String(64), comment="命中关键词类型")
    keyword = Column(String(64), comment="命中关键词")


class WarningEventMessage(Base):
    """
    预警和提醒消息接收
    """

    __tablename__ = 'warning_event_message'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    agent_id = Column(String(64), comment="坐席账号")
    agent_name = Column(String(64), comment="坐席姓名")
    call_id = Column(String(64), comment="通话ID")
    call_time = Column(DateTime, comment="来电时间")
    model_name = Column(String(64), comment="模型名称")
    model_id = Column(Integer, comment="模型名称")
    warning_name = Column(String(64), comment="提醒名称")
    reminder_id = Column(String(64), comment="提醒ID")
    warning = Column(Boolean, comment="是否预警类型")
    fly_screen = Column(Boolean, comment="飞屏类型")
    color = Column(String(16), comment="背景颜色")
    phone = Column(String(16), comment="客户手机号")
    create_time = Column(DateTime, default=datetime.datetime.now(),
                         comment="创建时间")
    update_time = Column(DateTime, onupdate=datetime.datetime.now(),
                         comment="更新时间")

    # time = Column(DateTime, nullable=False, comment="提醒时间")
    # ring_time = Column(DateTime, comment="响铃时间")
    # agent_account = Column(String(32), comment="坐席分析系统账号")
    # direction = Column(String(8), comment="呼叫方向")
    # total_time = Column(Integer, comment="通话时长")
    # caller = Column(String(16), comment="主叫号码")
    # called = Column(String(16), comment="被叫号码")
    # hit_word = Column(String(64), comment="命中模型内容")
    # keyword_type = Column(String(64), comment="命中关键词类型")
    # keyword = Column(String(64), comment="命中关键词")


class CallEventMessage(Base):
    __tablename__ = 'call_event_message'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    event = Column(String(16), default="newCall", comment="通话事件标识")
    call_id = Column(String(64), comment="通话ID")
    agent_id = Column(String(64), comment="坐席账号")
    call_time = Column(DateTime, comment="来电时间")
    ring_time = Column(DateTime, comment="响铃时间")
    create_time = Column(DateTime, default=datetime.datetime.now(),
                         comment="创建时间")
    direction = Column(String(8), comment="呼叫方向")
    caller = Column(String(16), comment="主叫号码")
    called = Column(String(16), comment="被叫号码")
    extra_info = Column(String(256), comment="额外信息")
    extension = Column(String(16), comment="预留字段")


class ResultEventMessage(Base):
    """
    识别结果事件
    """
    pass
    __tablename__ = "result_event_message"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    event = Column(String(16), default="newCall", comment="通话事件标识")
    call_id = Column(String(64), comment="通话ID")
    speech_id = Column(String(64), comment="通话ID")
    source = Column(String(64), comment="识别结果所属来源")
    result = Column(String(3000), comment="识别结果")


class HangupEventMessage(Base):
    __tablename__ = 'hangup_event_message'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    agent_id = Column(String(64), comment="坐席账号")
    agent_name = Column(String(64), comment="坐席姓名")
    account = Column(String(64), comment="坐席分析系统账号")
    extension = Column(String(64), comment="坐席分机号")
    ring_time = Column(DateTime, comment="响铃时间")
    call_id = Column(String(64), comment="通话ID")
    direction = Column(String(8), comment="呼叫方向")
    total_time = Column(Integer, comment="通话时长")
    caller = Column(String(16), comment="主叫号码")
    called = Column(String(16), comment="被叫号码")
    call_time = Column(DateTime, comment="来电时间")
    color = Column(String(16), comment="背景颜色")
    create_time = Column(DateTime, default=datetime.datetime.now(),
                         comment="创建时间")

    # hit_word = Column(String(64), comment="命中模型内容")
    # model_name = Column(String(64), comment="模型名称")
    # reminder_name = Column(String(64), comment="提醒名称")
    # reminder_id = Column(String(64), comment="提醒ID")
    # type = Column(Integer, comment="提醒类型")
    # time = Column(DateTime, nullable=False, comment="提醒时间")
    # phone = Column(String(16), comment="客户手机号")
    #
    # update_time = Column(DateTime, onupdate=datetime.datetime.now(),
    #                      comment="更新时间")
    #
    # agent_account = Column(String(32), comment="坐席分析系统账号")
    # keyword_type = Column(String(64), comment="命中关键词类型")
    # keyword = Column(String(64), comment="命中关键词")


# call_question = Table('call_question_association', Base.metadata,
#                       Column('call', ForeignKey('call.id'), primary_key=True),
#                       Column('question', ForeignKey('question.name'), primary_key=True),
#                       Column('intention', ForeignKey("intention.id"), primary_key=True),
#                       Column(DateTime, default=datetime.datetime.now(), comment="创建时间"),
#                       )


class CallModel(Base):
    __tablename__ = 'call_models'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    hangup_id = Column(Integer, index=True, comment="挂起事件ID")
    call_id = Column(String(64), comment="通话ID")
    model_name = Column(String(64), comment="模型名称")
    hit_word = Column(String(64), comment="命中模型内容")
    create_time = Column(DateTime, default=datetime.datetime.now(),
                         comment="创建时间")


class CallSentence(Base):
    __tablename__ = 'call_sentences'
    warning_id = Column(Integer, index=True, comment="预警时间ID")
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    call_id = Column(String(64), comment="通话ID")
    text = Column(String(64), comment="违规内容")
    role = Column(String(64), comment="句子所属角色")
    index = Column(Integer, comment="句子行号")


class Call(Base):
    """
    通话信息记录
    当 产生新的意图时, 更新通话的意图和意图号

    """
    __tablename__ = "call"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    call_id = Column(String(64), unique=True, comment="通话流水号")
    agent = Column(String(64), nullable=False, comment="坐席号")
    agent_name = Column(String(64), comment="坐席姓名")
    intention_id = Column(Integer, comment="意图号")
    intention_name = Column(String(64), comment="意图名称")
    phone = Column(String(16), comment="手机号")
    caller = Column(String(16), comment="主叫号码")
    called = Column(String(16), comment="被叫号码")
    direction = Column(String(16), comment="呼叫方向")
    call_time = Column(DateTime, comment="通话时间")
    duration = Column(Integer, comment="通话时长")
    ring_time = Column(DateTime, comment="响铃时间")
    create_time = Column(DateTime, default=datetime.datetime.now(),
                         comment="创建时间")
    update_time = Column(DateTime, onupdate=datetime.datetime.now(),
                         comment="更新时间")
    # questions = relationship("Call", secondary=call_question, back_populates="calls")
    # questions = relationship("Call")


class Question(Base):
    """
    问题列表, 每当检索到一条问题, 就创建一条问题
    """
    pass
    __tablename__ = "question"
    gid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id = Column(Integer, unique=True, nullable=True, comment="问题ID/知识ID", )
    name = Column(String(64), primary_key=True, unique=True, comment="问题名称")
    # knowledge_id = Column(Integer, unique=True, nullable=False, comment="知识ID")
    domain = Column(Integer, comment="所属知识库ID")
    type = Column(Integer, comment="问题类型")
    source = Column(Integer, comment="问题来源")
    access_times = Column(Integer, comment="点击次数")
    feedback = Column(Integer, comment="反馈状态")
    create_time = Column(DateTime, default=datetime.datetime.now(),
                         comment="创建时间")
    update_time = Column(DateTime, onupdate=datetime.datetime.now(),
                         comment="更新时间")
    # calls = relationship('Question', secondary=call_question, back_populates="questions")


class CallQuestion(Base):
    """
    通话问题列表
    """
    __tablename__ = "call_question"
    gid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question = Column(String(64), nullable=False, comment="问题名称")
    question_id = Column(String(64), nullable=False, comment="问题ID")
    question_source = Column(Integer, nullable=False, default=0, comment="问题来源")
    call_id = Column(String(64), nullable=False, comment="通话ID")
    agent = Column(String(16), comment="坐席ID")
    # intention = Column(Integer, ForeignKey('intenion'), nullable=False, comment="意图名称")
    intention_id = Column(Integer, comment="意图号")
    intention_name = Column(String(128), comment="意图名称")
    phone = Column(String(16), comment="客户手机号码")
    create_time = Column(DateTime, default=datetime.datetime.now(),
                         nullable=False, comment="创建时间")
    update_time = Column(DateTime, onupdate=datetime.datetime.now(),
                         comment="更新时间")


class Feedback(Base):
    """
    问题反馈统计
    """

    __tablename__ = "feedback"
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
    create_time = Column(DateTime, default=datetime.datetime.now(),
                         comment="创建时间")
    update_time = Column(DateTime, onupdate=datetime.datetime.now(),
                         comment="更新时间")
