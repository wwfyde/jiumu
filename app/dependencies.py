# Dependency
from app.db.database import SessionLocal


def get_db():
    """
    创建数据库连接会话
    :return:
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()