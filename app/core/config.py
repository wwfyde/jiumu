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


class QianxunPath(BaseSettings):
    warning: str = '/warning'
    result: str = "/recognizeResult/accessPoint"
    call: str = "/"


class Settings(BaseSettings):
    redis_dsn: RedisDsn = "redis://127.0.0.1:6379/1"
    mysql_dsn: MysqlDsn = "mysql+mysqldb://root:wawawa@127.0.0.1:43306/jiumu_helper"
    app_id: str = "421vaOJ0JMyNVJ6kMA"
    secret: str = "10Ti5rvwTHPReO70512a1ec25"
    sys_num: int = 1621329960501
    source_id: int = 215
    log_file_path: DirectoryPath = BASE_DIR.joinpath('log')
    client_id: str = "hjhj"
    yunwen_host: AnyUrl = "http://v5-gdc2-01.faqrobot.net"
    yunwen_path2: dict = {
        "search": "/chatbot/api/inputPrompt/{sys_num}",
        "token": "/admin/token/getToken",
        "intention": "/aiivr/ivr/v1/getVdnByPhone",
        "intention_feedback": "/aiivr/third/v1/feedbackVdn",
        "question": "/admin/private/jomoo/v1/getHotQuestion",
        "answer": "/admin/private/jomoo/v1/getHotQuestionInfo",
        "push": "/admin/private/jomoo/v1/addPushData",
    }
    yunwen_path: YunwenPath = YunwenPath()
    qianxun_host: AnyUrl = "http://127.0.0.1:8184"
    qianxun_path2 = {
        "warning": "/warning",
        "result": "/recognizeResult/accessPoint",
        "call": ""
    }
    qianxun_path: QianxunPath = QianxunPath()

    @classmethod
    def get_url(cls, host: AnyUrl, path: str):
        return host + path


settings = Settings()

if __name__ == '__main__':
    yunwen = YunwenPath()
    print(yunwen.intention_feedback)

    # print(type(yunwen.intention_feedback[0]), settings.qianxun_path.warnings)
    print(settings.qianxun_path.result)
    print(BASE_DIR.joinpath('log'))
