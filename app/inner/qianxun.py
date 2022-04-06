import json
import time
from typing import Optional, Union

import redis
import requests
import websocket

from app import settings
from app.inner import log
from app.utils.stomp import parse_frame, Stomp


def get_agent_info(agent: Union[str, int]) -> Optional[dict]:
    """
    根据坐席账号 获取坐席姓名等坐席信息
    :param agent:
    :return:
    """
    try:
        resp: dict = requests.get(
            settings.qianxun_host + settings.qianxun_path.agent,
            params=dict(account=agent,
                        user_token=settings.qianxun_token)
        ).json()

        if resp['functionResult'].upper() == "SUCCESS":
            log.info("获取坐席信息成功!")
            return dict(
                account=resp['data']["account"],
                name=resp['data']['username'],
                agent_id=resp['data']['agentId'],
                group=resp['data']['group'],
                role=resp['data']['roleName']
            )
        else:
            log.error(f"账号信息获取不成功! 错误代码: {resp['functionResult']}")

    except requests.exceptions.JSONDecodeError as json_err:
        log.error(f"接口未成功返回json字符串, 错误提示:{type(json_err)},  {json_err}")
    except Exception as exc:
        log.error(f"其他接口错误, 错误提示: {exc}")


def get_color_info(color_id: Optional[str] =
                   'HawkEye.HighLight.ExtractedColor') -> \
        Optional[str]:
    """

    :param color_id:
    :return:
    """
    r = redis.from_url(settings.redis_dsn, decode_responses=True)
    color = r.get(color_id)
    if color:
        log.info("从redis读取颜色信息")
        return color
    else:
        log.info("颜色信息已过期从")
        try:
            url = settings.qianxun_host + settings.qianxun_path.color
            resp: dict = requests.get(url, params=dict(userToken=settings.qianxun_token,
                                                       id=color_id)).json()

            if resp['functionResult'].upper() == "SUCCESS":
                log.info(f"获取颜色信息成功! 颜色信息: {resp['param']}")
                r.set(color_id, resp['param']['value'], ex=60 * 60)
                return resp['param']['value']
            else:
                log.error(f"颜色信息获取不成功! 错误代码: {resp['functionResult']}")
                return None
        except requests.exceptions.JSONDecodeError as json_err:
            log.error(f"接口未成功返回json字符串, 错误提示:{type(json_err)},  {json_err}")
            return None

        except Exception as exc:
            log.error(f"其他接口错误, 错误提示: {exc}")
            return None


def get_recent_call(agent: str) -> Optional[dict]:
    """
    获取坐席最近通话信息
    :return:
    """
    pass
    try:
        url: str = settings.qianxun_host + settings.qianxun_path.call.format(
            agent_id=agent)
        resp: dict = requests.get(url, params=dict(
            userToken=settings.qianxun_token)).json()

        if resp['functionResult'].upper() == "SUCCESS":
            if resp['data']['latestCall']:
                log.info(f"获取坐席{agent}最近通话信息! 通话信息: {resp['data']}")
                return dict(agent=resp['data']['latestCall']['agentId'],
                            agent_number=resp['data']['latestCall']['agentNumber'],
                            direction=resp['data']['latestCall']['callDirection'],
                            caller=resp['data']['latestCall']['callFromNumber'],
                            called=resp['data']['latestCall']['callToNumber'],
                            phone=resp['data']['latestCall']['customerNumber'],
                            call_id=resp['data']['latestCall']['callId'],
                            call_time=resp['data']['latestCall']['callTime'],
                            ring_time=resp['data']['latestCall']['ringTime'],
                            extension=resp['data']['latestCall']['extension'],
                            duration=resp['data']['latestCall']['duration'],
                            extra_info=resp['data']['latestCall']['extraInfo'],
                            is_online=resp['data']['online']
                            )
            else:
                log.info(f"当前坐席{agent}没有接通电话!")

        else:
            log.error(
                f"通话信息获取不成功! 错误代码: {resp['functionResult']}, 错误提示: {resp['message']}")
            return None
    except requests.exceptions.JSONDecodeError as json_err:
        log.error(f"接口未成功返回json字符串, 错误提示:{type(json_err)},  {json_err}")
        return None

    except Exception as exc:
        log.error(f"其他接口错误, 错误提示: {exc}")
        return None


def subscribe_speech_stream(agent: str, callback):
    websocket.enableTrace(True)
    token = settings.qianxun_token
    # token = '72bf0745-a04c-4a4b-9bff-cdfc4c0c1c94'
    stomp = Stomp(f"{settings.qianxun_host}/hawkeye/rest/v1/stomp?userToken={token}", sockjs=False, wss=False)
    stomp.connect()
    print("连接成功")
    stomp.subscribe(f"/topic/result/{agent}", callback)


if __name__ == '__main__':
    # resp= requests.get(settings.qianxun_path.agent,
    #                           params=dict(account=1234,
    #                                       user_token=settings.qianxun_token)
    #                           )
    # print(resp.status_code)
    print(get_agent_info(1000))
    print(get_color_info())
