import aioredis
import redis
import requests

# from ..config1 import config
from app.core.config import settings
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
                log.error(f"获取token失败, 接口返回了错误的提示, 错误代码: {resp.get('code')}")
                token = ''

        except Exception as exc:
            log.error(f"获取token失败,请求接口失败! 错误提示: {exc}")

            token = ''

        return token


def push_question_feedback(knowledge_id: int, types: int, feedback: int) -> bool:

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


if __name__ == '__main__':
    r = redis.from_url(settings.redis_dsn, decode_responses=True)
    r.set("a", 123)
    print(get_token())
    print(r.get("a"))
    print(r.get('token'))
