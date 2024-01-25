from datetime import datetime as dt

from sqlalchemy import String, Integer, DateTime, ForeignKey, create_engine, \
    Column
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

# postgresql://логин:пароль@имя хоста:порт/имя БД
engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres',
                       echo=True)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = 'users'
    tg_id = (Integer, primary_key=True)
    city = (String(60), nullable=False)
