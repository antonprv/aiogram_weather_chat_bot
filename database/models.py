from datetime import datetime as dt

from sqlalchemy import String, Integer, DateTime, ForeignKey, create_engine, \
    Column
from sqlalchemy.orm import relationship, declarative_base, sessionmaker


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    tg_id = Column(Integer, primary_key=True)
    city = Column(String(60), nullable=False)
    connection_date = Column(DateTime, default=dt.now, nullable=False)
    weather = relationship('WeatherReport',
                           back_populates='weathers', uselist=False,
                           lazy=True)

    def __repr__(self):
        return f'Человек {self.tg_id} из {self.city}'


class WeatherReport(Base):
    __tablename__ = 'weathers'
    id = Column(Integer, primary_key=True)
    temp = Column(Integer, nullable=False)
    feels_like = Column(Integer, nullable=False)
    wind_speed = Column(Integer, nullable=False)
    pressure_nm = Column(Integer, nullable=False)
    weather_date = Column(DateTime, ForeignKey('users.connection_date'),
                          nullable=False)
    city_id = Column(String(60), ForeignKey('users.city'), nullable=False)
    user = relationship('User', back_populates='weathers',
                        uselist=False, lazy=True)

    def __repr__(self):
        return f'В {self.city_id} сейчас {self.temp}'
