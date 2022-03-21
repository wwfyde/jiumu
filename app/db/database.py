from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# from app import config
# from sql_app import log


# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = f"mysql://{user}:{password}@{host}:{port}/{db}"
from app.core.config import settings
from app.db import log
SQLALCHEMY_DATABASE_URL = settings.mysql_dsn

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={},
    echo=True
)
log.info("初始化数据库引擎")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

if __name__ == '__main__':
    conn = engine.connect()

    cur = conn.execute("select @@VERSION")
    log.info("连接成功")
    print(cur.fetchone())
    pass
    db = SessionLocal()

