from typing import Optional, Union

import aioredis
import redis
import requests

# from ..config1 import config
from app.core.config import settings
from app.db import crud
from app.outer import log


def is_expired(gen_time: int, expire_time: int) -> bool:
    """
    判断token是否过期, 未过期时直接使用, 如果过期则重新获取
    :return:
    """

    return True


def get_token(fresh: bool = False) -> str:
    """
    获取access_token, 定时刷新token值

    :param fresh:
    :return:
    """
    # 从redis获取token值
    # redis = aioredis.from_url(f'redis://{username}:{password}@{host}/{db}', )
    # redis =redis.Redis()

    if not fresh:
        pass

    r = redis.from_url(settings.redis_dsn, decode_responses=True)
    token = r.get("token")
    if token:
        log.info("获取token成功, 直接从redis读取")
        return token

    else:

        data = {
            "appId": settings.app_id,
            "secret": settings.secret
        }
        try:
            resp: dict = requests.get(url=settings.yunwen_host + settings.yunwen_path.token, params=data).json()
            if resp.get('code') == 1:
                log.info("获取token成功!")
                data: dict = resp.get('data')
                token = data.get('accessToken')
                r.set("token", token, ex=60*60)
            else:
                log.error(f"获取token失败, 错误代码: {resp.get('code')}, 错误提示: {resp.get('message')}")
                token = ''

        except Exception as exc:
            log.error(f"获取token失败,请求接口失败! 错误提示: {exc}, Exception类型: {type(exc)}")

            token = ''

        return token


def push_question_feedback(knowledge_id: int, types: int, feedback: Optional[int] = None) -> bool:

    try:
        url: str = settings.yunwen_host + settings.yunwen_path.push
        resp: dict = requests.post(url, data=dict(
            knowledgeId=knowledge_id,
            type=types,
            feedback=feedback

        )).json()
        if resp['code'] == 200:
            log.info("提交反馈结果成功")

            return True
        else:
            log.error(f"提交返回结果失败, 错误提示: {resp['message']}")
            return False
    except Exception as exc:
        log.error(f"请求第三方接口失败! 错误提示: {exc}")
        return False


def search_question(question: str, source: int = 1):
    """

    :param question: 搜索问题
    :param source:
    :return:
    """
    data = []
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

    except requests.exceptions.ConnectionError as exc:
        log.error("请求云问接口失败! 请检查接口是否连通")

    return data


def get_intention_outer(phone: Union[int, str]):
    id: Optional[int] = None
    name: Optional[str] = ''
    try:
        url = settings.yunwen_host + settings.yunwen_path.intention
        resp: dict = requests.request(method='GET', url=url, params={
            'phone': phone,
            "sysNum": settings.sys_num,
            "access_token": get_token(),
        }).json()

        if resp['code'] == 1:
            log.info("意图获取成功")
            id = resp['data']['vdnNo']
            name = resp['data']['vdnName']

            pass
    except Exception as exc:
        log.error(f"请求第三方接口失败, 错误提示: {exc}")
    return id, name


if __name__ == '__main__':
    r = redis.from_url(settings.redis_dsn, decode_responses=True)
    r.set("a", 123)
    print(get_token())
    print(r.get("a"))
    print(r.get('token'))
