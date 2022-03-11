from typing import Optional, Union

import requests

from app import settings, log


def get_agent_info(agent: Union[str, int]) -> Optional[dict]:
    """
    根据坐席账号 获取坐席姓名等坐席信息
    :param agent:
    :return:
    """
    try:
        resp: dict = requests.get(settings.qianxun_host + settings.qianxun_path.agent,
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

    try:
        url = settings.qianxun_host + settings.qianxun_path.color
        resp: dict = requests.get(url, params=dict(id=color_id,
                                                   userToken=settings.qianxun_token)).json()

        if resp['functionResult'].upper() == "SUCCESS":
            log.info(f"获取颜色信息成功! 颜色信息: {resp['param']}")
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
        url: str = settings.qianxun_host + settings.qianxun_path.call.format(agent_id=agent)
        resp: dict = requests.get(url, params=dict(userToken=settings.qianxun_token)).json()

        if resp['functionResult'].upper() == "SUCCESS":
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
            log.error(f"通话信息获取不成功! 错误代码: {resp['functionResult']}, 错误提示: {resp['message']}")
            return None
    except requests.exceptions.JSONDecodeError as json_err:
        log.error(f"接口未成功返回json字符串, 错误提示:{type(json_err)},  {json_err}")
        return None

    except Exception as exc:
        log.error(f"其他接口错误, 错误提示: {exc}")
        return None


if __name__ == '__main__':
    # resp= requests.get(settings.qianxun_path.agent,
    #                           params=dict(account=1234,
    #                                       user_token=settings.qianxun_token)
    #                           )
    # print(resp.status_code)
    print(get_agent_info(1234))
