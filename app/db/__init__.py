import logging

from app.core.config import settings


def get_logger():
    log_format = '%(levelname)s %(asctime)s %(module)s %(lineno)d' \
             ' %(message)s %(filename)s %(name)s'
    logging.basicConfig(format=log_format, level=logging.WARN)
    handler = logging.FileHandler(filename=settings.log_file_path.joinpath('database.log'), encoding='utf-8')
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    logger = logging.getLogger('sqlalchemy')
    logger.addHandler(handler)
    logger.info("测试")
    return logger


log = get_logger()

if __name__ == '__main__':
    print(settings.log_file_path.joinpath('outer.log'))
