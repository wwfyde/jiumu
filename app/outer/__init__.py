import logging

from app.core.config import settings

FORMAT = '%(levelname)s: %(asctime)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
handler = logging.FileHandler(filename=settings.log_file_path.joinpath('outer.log'), encoding='utf-8')
formatter = logging.Formatter(FORMAT)
handler.setFormatter(formatter)
log = logging.getLogger(__name__)
log.addHandler(handler)

if __name__ == '__main__':
    print(settings.log_file_path.joinpath('outer.log'))
