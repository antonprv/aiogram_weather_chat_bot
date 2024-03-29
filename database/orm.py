from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import delete

from .models import Base, User, WeatherReport

from settings import database_config
from api_requests.request import get_weather

engine = create_engine(database_config.POSTGRE_URL, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def __current_user__(tg_id):
    return session.query(User).filter(User.tg_id == tg_id).first()

def __current_report__(report_id):
    return (session.query(WeatherReport).filter(WeatherReport.id == report_id)
            .first())


# Делаю запрос в БД, и вывожу первую строчку.
# Если строчка пустая - записываю пользователя в БД.
def add_user(tg_id, name):
    user = __current_user__(tg_id)
    if user is None:
        new_user = User(tg_id=tg_id, name=name)
        session.add(new_user)
        session.commit()


# Принимает id пользователя и город и потом ищет в БД пользователя
# с таким же id и устанавливает значение для его города проживания.
def set_user_city(tg_id, city):
    __current_user__(tg_id).city = city
    session.commit()


def get_user_city(tg_id):
    return __current_user__(tg_id).city


# По умолчанию функция берёт город, который пользователь указал как свой.
# Если указать кастомный город, то запишется, что вот такой-то юзер узнавал
# про погоду вот тут. Отношение one-to-many.
# Тк съехал на новый апи, при записи нужно конвертировать с mb на mhg
def save_report(tg_id, city=None):
    if city is None:
        city = get_user_city(tg_id)
    user = __current_user__(tg_id)
    data = get_weather(city)
    new_report = WeatherReport(user_id=user.id,
                               temp_c=data["current"]["temp_c"],
                               feelslike_c=data["current"]["feelslike_c"],
                               wind_kph=data["current"]["wind_kph"],
                               pressure_mm=round(
                                   (data["current"]["pressure_mb"] * 0.750062), 2),
                               city=city,
                               city_recognised=data["location"]["name"])
    session.add(new_report)
    session.commit()


def get_reports(tg_id):
    return __current_user__(tg_id).reports


def get_report_details(report_id):
    report = __current_report__(report_id=report_id)
    return report


def delete_report(report_id):
    report = session.get(WeatherReport, report_id)
    session.delete(report)
    session.commit()


def delete_all_reports(tg_id):
    usr_id = __current_user__(tg_id=tg_id).id
    del_reports = delete(WeatherReport).where(WeatherReport.user_id == usr_id)
    session.execute(del_reports)
    session.commit()


def get_all_users():
    return session.query(User).all()


def get_user_data(usr_id):
    return session.query(User).filter(User.id == usr_id).first()


def get_user_tg_id(usr_id):
    return get_user_data(usr_id=usr_id).tg_id