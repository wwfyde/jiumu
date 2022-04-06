import json
import logging
from datetime import datetime

from typing import Optional, List, Union

import redis
import requests
import xlsxwriter
from sqlalchemy import desc, func, extract
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks
from starlette.responses import HTMLResponse
from uvicorn import run
from fastapi import FastAPI, Query, Depends, Body, WebSocket
from fastapi.middleware.cors import CORSMiddleware

# from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import BaseModel

from app import log
# from app.config1 import config
from app.core.config import settings
from app.db.database import engine, SessionLocal
from app.dependencies import get_db
from app.inner.qianxun import get_agent_info, get_color_info, subscribe_speech_stream, get_recent_call
from app.outer.yunwen import get_token, push_question_feedback, search_question, get_intention_outer, push_click_event
from app.db import models, crud, schemas
from app.utils.stomp import parse_frame

# 初始化数据库
models.Base.metadata.create_all(bind=engine)

log.info("初始化数据库表成功!")
app = FastAPI(debug=True, title='九牧实时辅助助手', version='1.0.1')

# origins = [
#     "http://localhost",
#     "http://localhost:8187",
#     "http://10.222.26.183"
#     "http://10.222.26.183:8187"
#     "http://127.0.0.1:8187"
#     "http://127.0.0.1"
# ]
app.add_middleware(CORSMiddleware,
                   # allow_origins=origins,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )


# app.mount("/static", StaticFiles(directory="static"), name="static")


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: List[str] = []


@app.get("/")
def read_root():
    logging.info("hello, 世界!")
    return RedirectResponse('/docs')


@app.get("/items/{item_id}", description="查询元素", response_model=Item)
def read_item(item_id: int, s: str,
              q: Optional[str] = Query(None, title='Query String',
                                       description="查询字符串")):
    """
    意图查询接口
    :param item_id: 提示
    :param s: 必选参数
    :param q: 查询参数
    :return:
    """
    url: str = settings.yunwen_host + settings.yunwen_path.token
    token = get_token()
    log.info(f"获取token成功! token值: {token}")
    return {
        "item_id": item_id,
        "q": q,
        "token": token,
        "s": s,
    }


@app.get("/top", description="获取TOP问题, 意图热门知识排行")
def top(intention: str) -> dict:
    """
    根据意图获取热门知识排行榜
    :param intention:
    :return:
    """
    question_list = []

    try:

        url = settings.yunwen_host + settings.yunwen_path.top_question

        resp: dict = requests.get(url=url, params={
            "vdnNo": intention,
            "access_token": get_token(),
        }).json()
        log.debug(resp)
        if resp.get('code') == 1:
            log.debug(f"根据意图: {intention} 获取TOP问题成功!")
            raw_question_list: list = resp.get('data').get('questionList')
            for questions in raw_question_list:
                question_list.append(questions)
            return {
                "code": 1,
                "message": "success",
                "data": question_list,

            }

        else:
            log.error(f"第三方接口返回了错误信息.  代码: {resp['code']}, 提示: {resp['message']}")
            return {
                "code": 2,
                "message": resp['message'],
                "data": []

            }
            pass

    except Exception as exc:
        log.error(f"代码运行错误, 错误提示 {exc}")
        return {
            "code": 3,
            "message": f"代码错误: 错误提示{str(exc)}",
            "data": [],

        }


@app.get("/search", description="标准问题搜索")
def search(question: str) -> dict:
    """
     agent: Optional[str], call_id: Optional[str]
    根据搜索框获取问题标准答案
    此时不需要获取存入数据库
    :param question:
    :param agent: 坐席ID
    :param call_id: 通话流水号
    :return:
    """
    # TODO 搜索问题时标记问题来源
    data: list = search_question(question, source=1)

    return {
        "code": 1,
        "message": "success",
        "data": {
            "question_list": data
        }
    }


@app.get("/question", description="获取问题列表")
def get_questions(call_id: str,
                  agent: Union[int, str],
                  intention: Optional[Union[int, str]] = None,
                  db: Session = Depends(get_db)
                  ):
    """
    根据语音流获取问题列表
    :param agent:
    :param call_id:
    :param intention:
    :param db:
    :return:
    """
    questions = db.query(models.CallQuestion).filter(models.CallQuestion.call_id == call_id,
                                                     models.CallQuestion.agent == str(agent),
                                                     # models.CallQuestion.intention_id == intention
                                                     ).order_by(desc(models.CallQuestion.create_time)).all()

    log.info(f"问题列表:{questions}")

    # TODO 获取问题列表的方式
    return {
        "code": 1,
        "message": "success",
        "data": questions
    }


@app.post("/question", description="增加问题")
def create_question(question: schemas.CallQuestion,
                    db: Session = Depends(get_db)
                    ):
    """
    手动
    :param question:
    :param db:
    :return:
    """
    db_question = db.query(models.CallQuestion).filter(models.CallQuestion.call_id == question.call_id,
                                                       models.CallQuestion.agent == question.agent_id,
                                                       models.CallQuestion.intention_id == question.intention,
                                                       models.CallQuestion.question == question.question
                                                       ).first()
    db_question_full = models.CallQuestion(call_id=question.call_id,
                                           intention_id=question.intention,
                                           intention_name=question.intention_name,
                                           agent=question.agent_id,
                                           question_id=question.knowledge_id,
                                           question=question.question,
                                           question_source=question.source,
                                           )
    if not db_question:
        db.add(db_question_full)
        db.commit()
        db.refresh(db_question_full)
        log.info(f"agent:{question.agent_id},添加问题成功, 问体来源: 标准问题搜索, 问题名称: {question.question}")
    else:
        log.warning("该问题已经存在, 将不会添加到列表中")

    return {
        "code": 1,
        "message": "success",
        "data": db_question_full,
        "status": True,

    }
    pass


@app.delete("/question", description="删除问题")
def delete_question(question: schemas.CallQuestion,
                    db: Session = Depends(get_db)):
    db_question = db.query(models.CallQuestion).filter(models.CallQuestion.call_id == question.call_id,
                                                       models.CallQuestion.agent == question.agent_id,
                                                       # models.CallQuestion.intention_id == question.intention,
                                                       models.CallQuestion.question == question.question
                                                       ).first()
    if db_question:
        db.delete(db_question)
        db.commit()
        log.info("删除问题成功: ")
    else:
        log.warning("问题不存在, 删除失败")

    return {
        "code": 1,
        "message": "success",
        "data": db_question,
        "status": True
    }
    pass


@app.get("/answer", description="问题知识查询")
def get_answer(question: str,
               call_id: Optional[str] = None,
               source: Optional[int] = 1,
               agent: Optional[str] = Query(None, title="坐席账号",
                                            description="坐席账号 用于标识问题答案访问坐席"),
               db: Session = Depends(get_db)):
    """
    每次点击答案后, 进行一次统计, 返回反馈状态
    :param question: 标准问题名称
    :param call_id: 通话ID
    :param source: 问题来源 1: 语音流 2:检索问题 3: 热点问题
    :param agent:
    :param db: 依赖项
    :return:
    """
    if source in (1, 2):
        pass
    else:
        log.info("点击的是热点问题")
    try:
        url: str = settings.yunwen_host + settings.yunwen_path.answer.format(
            sys_num=settings.sys_num)
        resp: dict = requests.get(url, params={
            "s": "support",
            "access_token": get_token(),
            "question": question,
            "clientId": settings.client_id,
            "sourceId": settings.source_id,
        }).json()

        if resp.get("status") == 1:
            log.info(f"查询问题 [{question}] 的知识内容成功")
            raw_data: list = resp.get("data")
            data: list = []
            log.debug(f"返回的知识: {resp}")

            # 记录该问题被点击+1
            db_question: models.CallQuestion = db.query(models.CallQuestion).filter(
                models.CallQuestion.question == question,
                models.CallQuestion.call_id == call_id,
            ).first()

            if db_question:
                db_question.access_times += 1
                db.commit()
                db.refresh(db_question)
                log.debug(f"问题: {question}被访问, 记录访问状态+1")

                # 将问题点击事件推送到云问
                if source in (1, 2):
                    push_status = push_click_event(db_question.question_id, db_question.question)

                # 热点问题
                else:
                    push_status = push_question_feedback(db_question.question_id, 1)

                if push_status:
                    log.info("问题点击状态推送到云问成功")
                else:
                    log.warning("推送问题点击状态")
            else:
                # 热点问题不会被后端记录 但是依然需要反馈
                # 点击的是热点问题 需要反馈
                push_question_feedback(db_question.question_id, 1)

                log.warning(f"问题: {question}, 未被后端记录")

            # 拼接知识答案
            for raw_answer in raw_data:
                data.append(dict(
                    seed_question=raw_answer["seedQuestion"],
                    match_question=raw_answer["matchQuestion"],
                    answer_list=raw_answer["answerList"]
                ))
        else:
            log.error("接口请求错误")
            return {
                "code": 2,
                "message": "failed: 第三方接口返回了错误的代码",
                "data": "第三方接口返回了错误的代码",

            }

    except Exception as exc:
        log.error(f"请求云问接口失败! 请检查接口是否连通, 错误提示: {exc}")
        return {
            "code": 3,
            "message": "error: 请求云问接口失败",
            "data": "请求云问接口失败",

        }

    return {
        "code": 1,
        "message": "success",
        "data": data,
        "status": '',
    }


@app.get("/reminder", description="预警提醒")
def get_reminder(call_id: str, db: Session = Depends(get_db)):
    # TODO 获取最新的预警信息
    db_reminder = db.query(models.WarningEventMessage).filter(
        models.WarningEventMessage.call_id == call_id
    ).order_by(
        desc(models.WarningEventMessage.create_time)
    ).all()
    log.debug(f"预警提醒信息: {db_reminder}")
    return {
        'code': 1,
        "message": "success",
        "data": db_reminder,
    }


@app.get("/intention", description="意图获取")
def get_intention(phone: str = Query(..., title="手机号", max_length=16),
                  agent: Optional[str] = Query(None, title="坐席账号"),
                  db: Session =
                  Depends(
                      get_db)):
    # 根据坐席ID 获取手机号和通话ID 并存储到数据库

    # 访问第三方接口, 并将数据存储到数据库
    intention_id, intention_name = get_intention_outer(phone)
    if intention_id and intention_name:
        pass
        return {
            "code": 1,
            "message": "success",
            "data": {
                "intention": {
                    'id': intention_id,
                    'name': intention_name
                }
            },
        }
    else:
        return {
            "code": 2,
            "message": "error",
            "data": {},
        }


@app.get("/call", description="来电统计")
def get_call_times(agent: Union[int, str], phone: Optional[str] = None, db: Session = Depends(get_db)):
    # 获取url
    url = settings.qianxun_host + settings.qianxun_path.call

    # 根据挂断事件获取
    today = db.query(models.HangupEventMessage).filter(
        models.HangupEventMessage.agent_id == str(agent),
        func.date(models.HangupEventMessage.call_time) == datetime.today().date()
    ).count()
    month = db.query(models.HangupEventMessage).filter(
        models.HangupEventMessage.agent_id == str(agent),
        extract('year', models.HangupEventMessage.call_time) == datetime.today().date().year,
        extract('month', models.HangupEventMessage.call_time) == datetime.today().date().month,
    ).count()

    return {
        "code": 1,
        "message": "success",
        "data": {
            'today': today,
            'month': month
        }

    }


@app.post("/feedback", description="问题知识有效性反馈")
def question_feedback(feedback: schemas.Feedback,
                      db: Session = Depends(get_db)):
    """
    对问的知识答案进行反馈
    :param feedback:
    :param db:
    :return:
    """

    # 如果已经反馈过则不需要再次反馈
    # 判断问题是否反馈过
    db_call_question: models.CallQuestion = db.query(models.CallQuestion).filter(
        models.CallQuestion.question == feedback.question,
        models.CallQuestion.call_id == feedback.call_id,
    ).first()

    # 查询问题是否存在
    if db_call_question:
        if db_call_question.feedback == 0:
            log.info("提交反馈成功")
            db_call_question.feedback = feedback.feedback

            db.commit()
            db.refresh(db_call_question)

            # 将反馈结果推送到云问
            push_status = push_question_feedback(feedback.knowledge_id, 2,
                                                 feedback.feedback)

            status = 1
            description = "提交成功"
        else:
            log.debug(f"通话ID: {feedback.call_id}下的问题:{feedback.question}已经反馈过, 无须再次提交反馈")
            status = 0
            description = "该问题反馈结果已记录, 无须再次提交"
            push_status = False

    # 该问题不再问题标签列表中, 无法提交反馈
    else:
        log.info(f"问题: [{feedback.question}] 已提交过反馈, 无须再次提交")
        push_status = False
        status = -1
        description = "无效问题"
    return {
        "code": 1,
        "message": "success",
        "data": {
            "status": status,
            "description": description
        },
        "push": push_status,
    }


@app.post("/recognize")
async def recognition_result():
    return {}


@app.get("/chart/count")
def chart_statistics(date: Optional[str] = None, db: Session = Depends(get_db)):
    """
    报表统计当
    :param date: 指定统计哪一天的报表
    :param db: 数据库依赖
    :return:
    """
    # 获取坐席姓名
    # agent_id = 12345
    # agent_info = get_agent_info(agent_id)
    today = datetime.today().date()

    # 获取当天所有通话
    db_call = db.query(models.HangupEventMessage).filter(
        func.date(models.HangupEventMessage.call_time) == today)

    # 获取所有的坐席
    pass

    # 获取所有预警和提醒的名称
    db_reminder: Query = db.query(models.WarningEventMessage).filter(
        func.date(models.WarningEventMessage.call_time) == today)

    warnings, reminders = [], []
    for event in db_reminder:  # event models.WarningEventMessage
        if event.warning:
            log.info(event.warning)
            if event.warning_name not in warnings:
                warnings.append(event.warning_name)
        else:
            log.info(f"提醒:{event.warning}")

            if event.warning_name not in reminders:
                reminders.append(event.warning_name)

    # 构造headers
    headers = ['坐席姓名', '坐席ID', '通话总数', '提醒总数', '预警总数']

    for reminder in reminders:
        headers.append(f'提醒_{reminder}')
    for warning in warnings:
        headers.append(f'预警_{warning}')
    log.info(f"headers: {headers}")

    # 获取所有当天有通话的坐席
    agents = []
    for agent in db_call:
        if [agent.agent_name, agent.agent_id] not in agents:
            agents.append([agent.agent_name, agent.agent_id])

    log.debug(f"坐席列表: {agents}")

    # 统计坐席的所有数据
    data: List[dict] = []

    for row in agents:
        # 处理每个坐席的数据统计
        item = {
            headers[0]: row[0],
            headers[1]: row[1],
            headers[2]: db_call.filter(models.HangupEventMessage.agent_id == row[1]).count(),
            headers[3]: db_reminder.filter(
                models.WarningEventMessage.agent_id == row[1],
                models.WarningEventMessage.warning == 0,
            ).count(),
            headers[4]: db_reminder.filter(
                models.WarningEventMessage.agent_id == row[1],
                models.WarningEventMessage.warning == 1
            ).count(),
        }
        # 获取 提醒/预警总数
        for index, column in enumerate(headers[5:]):
            if column[:2] == "提醒":
                item[headers[5 + index]] = db_reminder.filter(
                    models.WarningEventMessage.agent_id == row[1],
                    models.WarningEventMessage.warning_name == column[3:]
                ).count()

            else:
                item[headers[5 + index]] = db_reminder.filter(
                    models.WarningEventMessage.agent_id == row[1],
                    models.WarningEventMessage.warning_name == column[3:]
                ).count()

        # 将 item 条件 data 中
        data.append(item)

    # 将文件写入
    file_path = settings.xlsx_file_path.joinpath(f"{today.strftime('%Y-%m-%d')}.xlsx")
    workbook = xlsxwriter.Workbook(file_path)
    worksheet = workbook.add_worksheet()

    # 将字典转换为列表
    statistics: list = []

    for data_item in data:
        container = []
        for key in headers:
            container.append(data_item[key])
        statistics.append(container)

    statistics.insert(0, headers)

    log.debug(f"表格二维表: {statistics}")

    for index, row in enumerate(statistics):
        worksheet.write_row(index, 0, row)

    workbook.close()

    return {
        "code": 1,
        "message": "success",
        "data": {
            "headers": headers,
            "data": data
        }
    }


@app.get("/chart/export")
def export_chart(date: Optional[str] = None, agent: Optional[Union[int, str]] = None):
    """
    将传入的数据生成xlsx文件
    :return:
    """
    today = datetime.today().date().strftime('%Y-%m-%d')

    # 获取当天的xlsx文件路径
    file_path = settings.xlsx_file_path.joinpath(f"{today}.xlsx")

    # 用于测试
    # data = [(1, 2, 3), (4, 5, 6)]
    # headers = ('一', '二', '三')
    # workbook = xlsxwriter.Workbook(file_path)
    # worksheet = workbook.add_worksheet()
    # statistics: list = [row for row in data]
    # statistics.insert(0, headers)
    # for index, row in enumerate(statistics):
    #     worksheet.write_row(index, 0, row)
    #
    # workbook.close()

    return FileResponse(file_path)


@app.post("/warning_event")
def receive_warning_event(data: dict = Body(...),
                          db: Session = Depends(get_db)):
    """

    :param db:
    :param data:
    :return:
    """
    """
    {
        "warningNotificationList": [
            {
                "agentId": "1000",
                "callId": "8c6d5237-a08c-4a71-adfd-df0a0ee37af0",
                "modelName": "欢迎",
                "warningName": "欢迎",
                "hitSentences": [
                    {
                        "text": "啊看欢迎致电玫赛德斯奔驰道路救援很高兴为您服务",
                        "role": "A",
                        "index": 0
                    }
                ],
                "warning": true,
                "flyScreen": false,
                "customerNum": "110000",
                "modelId": 335,
                "callTime": "2019-09-11 13:58:32"
            }
        ]
    }
    """
    for event in data['warningNotificationList']:
        multi_agent_info = get_agent_info(event["agentId"])

        db_warning = models.WarningEventMessage(
            agent_id=event["agentId"],
            agent_name=multi_agent_info['name'] if multi_agent_info else None,
            call_id=event["callId"],
            call_time=datetime.strptime(event["callTime"],
                                        '%Y-%m-%d %H:%M:%S') if event[
                "callTime"] else None,
            model_name=event["modelName"],
            model_id=event['modelId'],
            warning_name=event["warningName"],
            warning=event["warning"],
            color=get_color_info(),
            phone=event['customerNum'],
            fly_screen=event['flyScreen']

        )
        db.add(db_warning)
        db.commit()
        db.refresh(db_warning)
        for sentence in event['hitSentences']:
            db_call_sentence = models.CallSentence(
                warning_id=db_warning.id,
                call_id=event["callId"],
                text=sentence['text'],
                index=sentence['index'],
                role=sentence['role'])
            db.add(db_call_sentence)
            db.commit()
            db.refresh(db_call_sentence)

        log.info(f"接收预警推送消息成功, 并记录到数据库! {db_warning}, {db_warning.warning}")
        print(event)

    return {
        "functionResult": "SUCCESS",
        "message": "accepted"
    }
    pass


@app.post("/hangup_event")
def receive_hangup_event(
        data: dict = Body(...),
        db: Session = Depends(get_db)
):
    multi_agent_info = get_agent_info(data["agentId"])
    db_hangup = models.HangupEventMessage(
        agent_id=data["agentId"],
        agent_name=multi_agent_info['name'] if multi_agent_info else None,
        account=data['account'],
        extension=data['extension'],
        ring_time=datetime.strptime(data["ringTime"],
                                    '%Y-%m-%d %H:%M:%S') if data["ringTime"] else None,
        call_id=data["callId"],
        direction=data['direction'],
        total_time=data['duration'],
        caller=data['caller'],
        called=data['called'],
        call_time=datetime.strptime(data["callTime"],
                                    '%Y-%m-%d %H:%M:%S') if data[
            "callTime"] else None,
        color=get_color_info(),
    )
    db.add(db_hangup)
    db.commit()
    db.refresh(db_hangup)
    if data.get('hitModels'):
        for model in data['hitModels']:
            db_call_model = models.CallModel(
                hangup_id=db_hangup.id,
                call_id=data['callId'],
                model_name=model['modelName'],
                hit_word=model['hitWords'])
            db.add(db_call_model)
            db.commit()
            db.refresh(db_call_model)
    else:
        log.error("配置未开启! 未推送模型命中、确认关键词结果")
    log.info(f"接收挂断事件成功, 并记录到数据库! {data}")
    pass
    return {
        "functionResult": "SUCCESS",
        "message": "accepted"
    }


def on_speech_stream(msg: str):
    """
    回调时间, 用于解析数据库
    :param db:
    :param msg:
    :return:
    """
    print("正在订阅")
    print("MESSAGE: " + msg)
    command, header, body = parse_frame(msg)
    # command, header, body = ('MESSAGE', {}, msg)

    if command == "MESSAGE":
        speech_stream: dict = json.loads(body)

        if speech_stream['status'] == 'continue':

            # 根据呼叫方向确定客户号码
            phone = speech_stream['callFromNumber'] if speech_stream['direction'] == 'inbound' \
                else speech_stream['callToNumber']

            # 获取意图
            intention_id, intention_name = get_intention_outer(phone)

            for raw_message in speech_stream['messages']:
                if raw_message['type'] == 'text':
                    text: str = raw_message['info']['text']
                    #  查询问题知识库
                    questions: list = search_question(text, source=2)
                    # questions: list = [
                    #     {'question': '测试', 'knowledge_id': 1243},
                    #     {'question': '测试2', 'knowledge_id': 12434},
                    # ]

                    # TODO 将问题列表添加到数据库
                    for question in questions:
                        db_question = models.CallQuestion(question=question['question'],
                                                          question_id=question['knowledge_id'],
                                                          question_source=1,
                                                          call_id=speech_stream['callId'],
                                                          agent=speech_stream['agentId'],
                                                          intention_id=intention_id,
                                                          intention_name=intention_name,
                                                          phone=phone)
                        db: Session = SessionLocal()
                        log.info("添加问题到数据库")
                        db.add(db_question)
                        db.commit()
                        db.refresh(db_question)

    elif command == "CONNECTED":
        pass
    else:
        pass


@app.get("/speech_stream")
async def receive_speech_stream(agent: str, background_tasks: BackgroundTasks, intention: Optional[str] = None,
                                db: Session = Depends(get_db)):
    log.info(f"正在获取坐席:{agent}下的实时语音流信息")
    # msg = """{"agentId":"9999","callId":"eb4da0f8-0ddb-4b07-aa3e-5e18bacad2eb",
    # "direction":"inbound","extension":"9999","callFromNumber":"1****000","callToNumber":"999","beginTime":"2022-03-18
    # 13:50:27","status":"continue","messages":[{"type":"text","info":{"decided":false,"role":"customer",
    # "duration":56052,"text":"是吧你告诉他","time":"55260,56052","index":23,"offset":0,"wordBeginTime":55260,
    # "wordEndTime":56052}}]}"""

    # on_speech_stream(msg=msg)
    # subscribe_speech_stream(agent, on_speech_stream)
    background_tasks.add_task(subscribe_speech_stream, agent, on_speech_stream)
    log.info("创建后台任务成功")

    return {
        "code": 1,
        "message": "success",
        "data": '',
        "status": True
    }


@app.get("/demo")
def get_demo(demo: Optional[str] = None, db: Session = Depends(get_db)):
    db = db.query(models.Demo).all()
    return db


@app.post("/demo")
def create_demo(demo: schemas.Demo, db: Session = Depends(get_db)):
    exists = db.query(models.Demo).filter(
        models.Demo.name == demo.name
    ).first()

    if not exists:

        db_demo = crud.create_demo(db, demo)
        db.commit()
        db.refresh(db_demo)
        log.info("新建数据成功!")
    else:
        log.info("数据已经存在, 将不会提交或更新")

    return {
        "code": 1,
        "message": "success",
        "data": ''
    }


@app.put("/demo")
def update_demo(demo: schemas.Demo, db: Session = Depends(get_db)):
    db_demo = crud.update_demo(db, demo)
    db.commit()
    db.refresh(db_demo)
    log.info("更新数据成功!")
    # exists = db.query(models.Demo).filter_by(name=demo.name).first()
    #
    # if not exists:
    #
    #     db_demo = crud.update_demo(db, demo)
    #     db.commit()
    #     db.refresh(db_demo)
    #     log.info("更新数据成功!")
    # else:
    #     log.info("数据已经存在, 将不会提交或更新")

    return {
        "code": 1,
        "message": "success",
        "data": ''
    }


@app.get("/call_info")
def get_call_info(agent: Union[str, int], db: Session = Depends(get_db)):
    """
    根据坐席获取用户的基础信息
    :param db:
    :param agent:
    :return:
    """
    # 获取
    info: dict = get_recent_call(agent)
    # 示例

    # dict(agent=resp['data']['latestCall']['agentId'],
    #      agent_number=resp['data']['latestCall']['agentNumber'],
    #      direction=resp['data']['latestCall']['callDirection'],
    #      caller=resp['data']['latestCall']['callFromNumber'],
    #      called=resp['data']['latestCall']['callToNumber'],
    #      phone=resp['data']['latestCall']['customerNumber'],
    #      call_id=resp['data']['latestCall']['callId'],
    #      call_time=resp['data']['latestCall']['callTime'],
    #      ring_time=resp['data']['latestCall']['ringTime'],
    #      extension=resp['data']['latestCall']['extension'],
    #      duration=resp['data']['latestCall']['duration'],
    #      extra_info=resp['data']['latestCall']['extraInfo'],
    #      is_online=resp['data']['online']
    #      )
    if info:
        # 获取账号意图
        intention_id, intention_name = get_intention_outer(info['phone'])

        r = redis.from_url(settings.redis_dsn, decode_responses=True)
        r.hset(info['call_id'], 'agent', info['agent'])
        r.hset(info['call_id'], 'agent_number', info['agent_number'])
        r.hset(info['call_id'], 'direction', info['direction'])
        r.hset(info['call_id'], 'caller', info['caller'])
        r.hset(info['call_id'], 'called', info['called'])
        r.hset(info['call_id'], 'phone', info['phone'])
        r.hset(info['call_id'], 'call_id', info['call_id'])
        r.hset(info['call_id'], 'call_time', info['call_time'])
        r.hset(info['call_id'], 'ring_time', info['ring_time'])
        r.hset(info['call_id'], 'extension', info['extension'])
        r.hset(info['call_id'], 'duration', info['duration'])
        # 是字典 暂时不存储
        # r.hset(info['call_id'], 'extra_info', info['extra_info'])
        r.hset(info['call_id'], 'is_online', str(info['is_online']))
        if intention_id:
            r.hset(info['call_id'], 'intention_id', intention_id)
        if intention_name:
            r.hset(info['call_id'], 'intention_name', intention_name)
        db_call = models.Call(
            agent=info['agent'],
            caller=info['caller'],
            called=info['called'],
            direction=info['direction'],
            duration=int(info['duration']) if info['duration'] else 0,
            phone=info['phone'],
            call_id=info['call_id'],
            intention_id=intention_id,
            intention_name=intention_name,
            call_time=datetime.strptime(info['call_time'], '%Y-%m-%d %H:%M:%S') if info['call_time'] else None,
            ring_time=datetime.strptime(info['ring_time'], '%Y-%m-%d %H:%M:%S') if info['ring_time'] else None,
        )
        exists = db.query(models.Call).filter(models.Call.call_id == info['call_id']).first()
        if not exists:
            log.info(f"根据坐席ID: {agent}获取通话{info}信息成功")
            db.add(db_call)
            db.commit()
            db.refresh(db_call)
        else:
            log.debug("通话信息已存在无须再次插入")
            pass

        return {
            'code': 1,
            'message': 'success',
            'data': db_call,
        }
    else:

        log.error(f"获取坐席: {agent}最近通话信息失败!")
        return {
            'code': 2,
            'message': 'failed',
            'data': {},
        }


@app.get("/caller")
def get_call_info2(agent: str):
    """
    获取当前通话的相关信息
    :param agent:
    :return:
    """

    # 获取最近通话
    pass
    return {}


#
# async def fake_video_streamer():
#     for i in range(10):
#         yield b"some fake video bytes"
#
#
# @app.get("/demo_stream")
# async def main():
#     return StreamingResponse(fake_video_streamer())
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://127.0.0.1:8188/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/ws_demo")
async def ws_client():
    return HTMLResponse(html)


@app.websocket("/recognition_event")
async def ws_server(websocket: WebSocket, ):
    """
    接收客户事件推送
    :param websocket:
    :return:
    """
    await websocket.accept()
    while True:
        data: dict = await websocket.receive_json()
        # TODO 解析语音流信息, 并存储到数据库
        if data['']:
            pass
        log.info(f"接收信息成功:{data}")
        await websocket.send_text(f"Message text was: {type(data)}")


if __name__ == "__main__":
    run(app='main:app', reload=True, port=8199, workers=4)
    pass
    # db: Session = Depends(get_db)
    # data = db.query(models.Demo)
    # print(data)
