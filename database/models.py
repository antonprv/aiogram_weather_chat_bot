from datetime import datetime as dt

from sqlalchemy import String, Integer, DateTime, ForeignKey, Column, \
    BigInteger
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    connection_date = Column(DateTime, default=dt.now, nullable=False)
    tg_id = Column(BigInteger, nullable=False)
    city = Column(String)
    reports = relationship('WeatherReports', backref='report',
                           lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return self.tg_id


class WeatherReport(Base):
    __tablename__ = 'WeatherReports'
    id = Column(Integer, ForeignKey('Users.id'), primary_key=True,
                nullable=False)
    date = Column(DateTime, default=dt.now, nullable=False)
    temp = Column(Integer, nullable=False)
    feels_like = Column(Integer, nullable=False)
    wind_speed = Column(Integer, nullable=False)
    pressure_mm = Column(String, nullable=False)
    city = Column(String, nullable=False)

    def __repr__(self):
        return self.city
