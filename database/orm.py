from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, User

from settings import database_config

engine = create_engine(database_config.POSTGRE_URL, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


# Делаю запрос в БД, и вывожу первую строчку.
# Если строчка пустая - записываю пользователя в БД.
def add_user(tg_id):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    if user is None:
        new_user = User(tg_id=tg_id)
        session.add(new_user)
        session.commit()
