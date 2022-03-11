import logging
from datetime import datetime

from typing import Optional, List, Union

import requests
from sqlalchemy import desc
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import StreamingResponse
from uvicorn import run
from fastapi import FastAPI, Query, Depends, Body
from fastapi.middleware.cors import CORSMiddleware

# from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import BaseModel

from app import log
# from app.config1 import config
from app.core.config import settings
from app.db.database import engine
from app.dependencies import get_db
from app.inner.qianxun import get_agent_info, get_color_info
from app.outer.yunwen import get_token, push_question_feedback
from app.db import models, crud, schemas

models.Base.metadata.create_all(bind=engine)

log.info("初始化数据库表成功!")
app = FastAPI(debug=True, title='九牧实时辅助助手', version='1.0.1')
app.add_middleware(CORSMiddleware,
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
    url: str = settings.yunwen_host + settings.yunwen_api.get("token")
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
    try:

        url = settings.yunwen_host + settings.yunwen_path.top

        resp: dict = requests.get(url=url, params={
            "vdnNo": intention,
            "access_token": get_token(),
        }).json()
        log.debug(resp)
        if resp.get('code') == 1:
            raw_question_list: list = resp.get('data').get('questionList')
            question_list = []
            for questions in raw_question_list:
                question_list.append(questions)
        else:
            log.error("第三方接口连接失败")

            pass

    except Exception as exc:
        log.error(f"接口连接失败, 错误提示 {exc}")

    return {

    }


@app.get("/search", description="标准问题搜索")
def search(question: str) -> dict:
    """
     agent: Optional[str], call_id: Optional[str]
    根据搜索框获取问题标准答案
    :param question:
    :param agent: 坐席ID
    :param call_id: 通话流水号
    :return:
    """

    try:
        url: str = settings.yunwen_host + settings.yunwen_path.search.format(
            sys_num=settings.sys_num)
        resp: dict = requests.get(url, params={
            "access_token": get_token(),
            "sourceId": settings.source_id,
            "clientId": settings.client_id,
            "question": question,
        }).json()

        if resp.get('code') == 1:
            log.info(f"搜索标准问题成功, 内容: {resp}")
            raw_data: list = resp.get('data').get('items')
            data = []
            if raw_data:
                for raw_question in raw_data:
                    #
                    crud.get_question()
                    data.append(dict(knowledge_id=raw_question.get('itemId'),
                                     question=raw_question.get('content'),
                                     question_desc=raw_question.get(
                                         'showContent')))
            else:
                log.info("未搜索到标准问题")
        else:
            log.error("接口返回了错误的信息,")
            return {
                "code": 3,
                "message": "failed",
                "data": [],
            }
    except requests.exceptions.ConnectionError as exc:
        log.error("请求云问接口失败! 请检查接口是否连通")
        return {
            "code": 2,
            "message": "error",
            "data": "",

        }
    return {
        "code": 1,
        "message": "success",
        "data": {
            "question_list": data
        }
    }


@app.get("/question", description="获取问题列表")
def get_question(call_id: str,
                 intention: str,
                 db: Session = Depends(get_db)
                 ):
    # TODO 获取问题列表的方式
    return {
        "code": 1,
        "message": "success",
        "data": ''
    }


@app.post("/question", description="增加问题")
def create_question(question: str,
                    call_id: str,
                    intention: str,
                    knowledge_id: int,
                    question_id: Optional[int] = None,
                    db: Session = Depends(get_db)
                    ):
    db_question = models.Question(call_id=call_id,
                                  intention=intention,
                                  name=question,
                                  qid=question_id,
                                  knowledge_id=knowledge_id
                                  )

    db.add(db_question)
    pass


@app.delete("/question", description="删除问题")
def delete_question():
    pass


@app.get("/answer", description="问题知识查询")
def get_answer(question: str,
               agent: Optional[str] = Query(None, title="坐席账号",
                                            description="坐席账号 用于标识问题答案访问坐席"),
               db: Session = Depends(get_db)):
    """
    每次点击答案后, 进行一次统计
    :param question: 标准问题名称
    :param agent:
    :param db: 依赖项
    :return:
    """
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
            log.info("请求第三方接口成功")
            raw_data: list = resp.get("data")
            data: list = []

            # TODO 记录该问题被点击

            for raw_answer in raw_data:
                data.append(dict(
                    seed_question=raw_answer["seedQuestion"],
                    match_question=raw_answer["matchQuestion"],
                    answer_list=raw_answer["answerList"]
                ))
        else:
            log.error("接口请求错误")
            return {
                "code": 3,
                "message": "failed: 第三方接口返回了错误的代码",
                "data": "第三方接口返回了错误的代码",

            }

    except Exception as exc:
        log.error(f"请求云问接口失败! 请检查接口是否连通, 错误提示: {exc}")
        return {
            "code": 2,
            "message": "error: 请求云问接口失败",
            "data": "请求云问接口失败",

        }

    return {
        "code": 1,
        "message": "success",
        "data": data,
    }


@app.get("/reminder", description="预警提醒")
def get_reminder():
    return {}


@app.get("/intention", description="意图获取")
def get_intention(phone: str = Query(..., title="手机号", max_length=16),
                  agent: Optional[str] = Query(None, title="坐席账号"),
                  db: Session =
                  Depends(
                      get_db)):
    # 根据坐席ID 获取手机号和通话ID 并存储到数据库

    # 访问第三方接口, 并将数据存储到数据库
    try:
        url = settings.yunwen_host + settings.yunwen_path.intention
        resp: dict = requests.request(method='GET', url=url, params={
            'phone': phone,
            "sysNum": settings.sys_num,
            "access_token": get_token(),
        }).json()

        if resp['code'] == 1:
            log.info("意图获取成功")
            data = resp['data']
            pass
    except Exception as exc:
        log.error(f"请求第三方接口失败, 错误提示: {exc}")
        return {
            'code': 2,
            'message': 'error',
            "data": ''
        }

    # 根据agent 获取 通话ID和客户手机号
    db.query(models.Intention).filter(
        models.Intention.agent == agent).order_by(
        desc(models.Intention.read_time))
    return {
        "code": 1,
        "message": "success",
        "data": data,
    }


@app.get("/call", description="来电统计")
def get_call_times(phone: str, db: Session = Depends(get_db)):
    # 获取url
    url = settings.qianxun_host + settings.qianxun_path.call
    data = dict(today='', month='')
    return {
        "code": 1,
        "message": "success",
        "data": data

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
    exists = db.query(models.Feedback).filter_by(
        question=feedback.question).first()
    log.debug(f"查询结果: {exists}")
    if not exists:
        log.info("提交反馈成功")
        db_feedback = models.Feedback(question=feedback.question,
                                      knowledge_id=feedback.knowledge_id,
                                      feedback=feedback.feedback,
                                      agent=feedback.agent)
        db.add(db_feedback)
        db.commit()
        db.refresh(db_feedback)

        # 将反馈结果推送到云问
        push_status = push_question_feedback(feedback.knowledge_id, 2,
                                             feedback.feedback)

        if db_feedback:
            status = 1
            description = "提交成功"
        else:
            status = 0
            description = "提交失败"

    else:
        log.info(f"问题: [{feedback.question}] 已提交过反馈, 无须再次提交")
        push_status = False
        status = 2
        description = "该问题反馈结果已记录, 无须再次提交"
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


@app.get("/chart/statistics")
def chart_statistics():
    # 获取坐席姓名
    agent_id = 12345
    agent_info = get_agent_info(agent_id)

    if agent_info:
        log.info("获取坐席姓名成功")
        name = agent_info['name']
    else:
        log.warning("未获取到用户姓名, 将以坐席ID代替")
        name = agent_id

    return {}


# 响应文件
@app.post("/chart/export")
def export_chart():
    file_path = "file.md"

    return FileResponse(file_path)


@app.post("/reminder_receiver")
def receive_reminder():
    """
    接口用于接收预警提醒
    :return:
    """
    pass
    return


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

        log.info("接收推送消息成功, 并记录到数据库")
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
        ring_time=data['ringTime'],
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
    for model in data['hitModels']:
        db_call_model = models.CallModel(
            hangup_id=db_hangup.id,
            call_id=data['callId'],
            model_name=model['modelName'],
            hit_word=model['hitWords'])
        db.add(db_call_model)
        db.commit()
        db.refresh(db_call_model)
    log.info("接收推送消息成功, 并记录到数据库")
    pass
    return {
        "functionResult": "SUCCESS",
        "message": "accepted"
    }


@app.get("/demo")
def get_demo(demo: Optional[str] = None, db: Session = Depends(get_db)):
    db = db.query(models.Demo).all()
    return db


@app.post("/demo")
def create_demo(demo: schemas.Demo, db: Session = Depends(get_db)):
    exists = db.query(models.Demo).filter_by(name=demo.name).first()

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


@app.get("/base_info/{agent}")
def get_base_info(agent: Union[str, int]):
    pass
    return {}


@app.get("/caller")
def get_call_info(agent: str):
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


if __name__ == "__main__":
    run(app='main:app', reload=True, port=8199, workers=4)
