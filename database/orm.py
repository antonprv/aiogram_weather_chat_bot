from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, User, WeatherReport

from settings import database_config
from api_requests.request import get_weather

engine = create_engine(database_config.POSTGRE_URL, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


# Делаю запрос в БД, и вывожу первую строчку.
# Если строчка пустая - записываю пользователя в БД.
def add_user(tg_id, name):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    if user is None:
        new_user = User(tg_id=tg_id, name=name)
        session.add(new_user)
        session.commit()


# Принимает id пользователя и город и потом ищет в БД пользователя
# с таким же id и устанавливает значение для его города проживания.
def set_user_city(tg_id, city):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    user.city = city
    session.commit()


def get_user_city(tg_id):
    session = Session()
    user = session.query(User).filter(User.tg_id == tg_id).first()

    return user.city


# По умолчанию функция берёт город, который пользователь указал как свой.
# Если указать кастомный город, то запишется, что вот такой-то юзер узнавал
# про погоду вот тут. Отношение one-to-many.
def save_report(tg_id, city=None):
    session = Session()
    if city is None:
        city = get_user_city(tg_id)
    data = get_weather(city)
    new_report = WeatherReport(temp=data["temp"],
                               feels_like=data["feels_like"],
                               wind_speed=data["wind_speed"],
                               pressure_mm=data["pressure_mm"],
                               city=city)
    session.add(new_report)
    session.commit()
