from pathlib import Path

from pydantic import (
    BaseModel,
    BaseSettings,
    BaseConfig,
    RedisDsn,
    AnyUrl,
    FilePath,
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
    search: str = "/chatbot/api/inputPrompt/{sys_num}"
    answer: str = "/chatbot/api/v5/chat/{sys_num}"
    token: str = "/admin/token/getToken"
    intention: str = "/aiivr/ivr/v1/getVdnByPhone"
    intention_feedback: str = "/aiivr/third/v1/feedbackVdn"
    question: str = "/admin/private/jomoo/v1/getHotQuestion"
    top: str = "/admin/private/jomoo/v1/getHotQuestion"
    push: str = "/admin/private/jomoo/v1/addPushData"

    # 语音流地址
    call_stream: str = "/hawkeye/rest/v1/stomp?userToken={user_token}"
    # 订阅队列
    call_queue: str = "/topic/result/{agent_id}"


class QianxunPath(BaseSettings):
    warning: str = '/warning'
    result: str = "/recognizeResult/accessPoint"

    # 获取坐席的最近通话信息
    call: str = "/hawkeye/rest/v1/agentLatestCall/{agent_id}"

    # 获取坐席账号信息
    agent: str = "/hawkeye/rest/v1/match/user"

    # color 高亮颜色信息展示
    color: str = "/param"


class Settings(BaseSettings):
    redis_dsn: RedisDsn = "redis://127.0.0.1:6379/1"
    mysql_dsn: MysqlDsn = "mysql+mysqldb://root:wawawa@127.0.0.1:43306" \
                          "/jiumu_helper?charset=utf8mb4"

    # mysql_dsn: MysqlDsn = "mysql+pymysql://root:wawawa@127.0.0.1:43306/jiumu_helper"
    log_file_path: DirectoryPath = BASE_DIR.joinpath('log')
    xlsx_file_path: DirectoryPath = BASE_DIR.joinpath('xlsx')

    # 外部接口: 云问相关配置
    app_id: str = "421vaOJ0JMyNVJ6kMA"
    secret: str = "10Ti5rvwTHPReO70512a1ec25"
    sys_num: int = 1621329960501
    source_id: int = 215
    client_id: str = "hjhj"
    yunwen_host: AnyUrl = "http://v5-gdc2-01.faqrobot.net"
    yunwen_path: YunwenPath = YunwenPath()

    # 内部接口: 千寻相关配置
    qianxun_token: str = "72bf0745-a04c-4a4b-9bff-cdfc4c0c1c94"
    qianxun_host: AnyUrl = "http://192.168.129.176:8186"
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

