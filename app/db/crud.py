from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_intention(db: Session, agent: str):
    return db.query(models.Intention).filter(models.Intention.agent == agent)


def create_demo(db: Session, demo: schemas.Demo):

    db_demo = models.Demo(name=demo.name, type=demo.type, desc=demo.desc)
    db.add(db_demo)
    # db.refresh(db_demo)
    return db_demo


def update_demo(db: Session, demo: schemas.Demo):

    # db_demo = models.Demo(name=demo.name, type=demo.type, desc=demo.desc)
    # db.add(db_demo)
    db_demo = db.query(models.Demo).filter_by(name=demo.name).first()
    db_demo.desc = demo.desc

    return db_demo


def get_question(db: Session, question: str):

    return db.query(models.Question).filter(models.Question.question == question).first()


def get_question_by_id(db: Session, id: str):
    return db.query(models.Question).filter(models.Question.id == id).first()


def get_question_by_knowledge_id(db: Session, knowledge_id: str):
    """

    :param db:
    :param knowledge_id:
    :return:
    """
    return db.query(models.Question).filter(models.Question.knowledge_id == knowledge_id).first()
