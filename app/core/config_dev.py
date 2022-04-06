from pathlib import Path

from pydantic import (
    BaseSettings,
    RedisDsn,
    AnyUrl,
    DirectoryPath,

)

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = BASE_DIR.parent


class MysqlDsn(AnyUrl):
    allowed_schemes = {
        'mysql+mysqldb',
        'mysql+pymysql'
    }


class YunwenPath(BaseSettings):

    # 问题搜索
    search: str = "/chatbot/api/inputPrompt/{sys_num}"

    # 知识搜索
    answer: str = "/chatbot/api/v5/chat/{sys_num}"

    # 获取token
    token: str = "/admin/token/getToken"

    # 获取意图
    intention: str = "/aiivr/third/v1/getVdnByPhone"

    # 获取TOP热点问题
    top_question: str = "/admin/private/jomoo/v1/getHotQuestion"

    # 获取TOP热点问题的详情内容
    top_question_info: str = "/admin/private/jomoo/v1/getHotQuestionInfo"

    # 推送热点问题和 点击反馈
    push: str = "/admin/private/jomoo/v1/addPushData"

    # 标准问题点击反馈
    hit_question_event: str = "/admin/private/jomoo/v1/hitQuestion?access_token={token}"


class QianxunPath(BaseSettings):
    warning: str = '/warning'
    result: str = "/recognizeResult/accessPoint"

    # 获取坐席的最近通话信息
    call: str = "/hawkeye/rest/v1/agentLatestCall/{agent_id}"

    # 获取坐席账号信息
    agent: str = "/hawkeye/rest/v1/match/user"

    # color 高亮颜色信息展示
    color: str = "/param"

    # 语音流地址  已弃用
    call_stream: str = "/hawkeye/rest/v1/stomp?userToken={user_token}"
    # 订阅队列  已弃用
    call_queue: str = "/topic/result/{agent_id}"


class Settings(BaseSettings):
    redis_dsn: RedisDsn = "redis://127.0.0.1:6379/1"
    mysql_dsn: MysqlDsn = "mysql+pymysql://root:admin@127.0.0.1:3306" \
                          "/jiumu_helper?charset=utf8mb4"

    # mysql_dsn: MysqlDsn = "mysql+pymysql://root:wawawa@127.0.0.1:43306/jiumu_helper"
    log_file_path: DirectoryPath = BASE_DIR.joinpath('log')
    xlsx_file_path: DirectoryPath = BASE_DIR.joinpath('xlsx')

    # 外部接口: 云问相关配置
    app_id: str = "83BLjz5H2VUaOWSFT5"
    secret: str = "10BTMRki3bAY61o8dd24c45a7"
    sys_num: int = 1645755108284
    source_id: int = 133
    client_id: str = "hjhj"
    yunwen_host: AnyUrl = "http://10.222.26.19"
    yunwen_path: YunwenPath = YunwenPath()

    # 内部接口: 千寻相关配置
    qianxun_token: str = "38f6cf95-2282-4b5b-b457-42dd1bfedc99"
    qianxun_host: AnyUrl = "http://127.0.0.1:8186"
    qianxun_path: QianxunPath = QianxunPath()

    @classmethod
    def get_url(cls, host: AnyUrl, path: str):
        return host + path


settings = Settings()

if __name__ == '__main__':
    yunwen = YunwenPath()
    print(yunwen.intention_feedback)

    # print(type(yunwen.intention_feedback[0]), settings.qianxun_path.warnings)
    print(settings.qianxun_path.call.format(agent_id='12333'))

    # print(Path().joinpath(settings.qianxun_host, settings.qianxun_path.call.format(agent_id=1234)))
