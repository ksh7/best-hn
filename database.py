from datetime import date

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base


db_engine = create_engine('sqlite:///hackernewsbest.db')

Base = declarative_base()


class HackernewsBest(Base):
    __tablename__ = 'hackernews_best'

    id = Column(Integer, primary_key=True)
    news_id = Column(String)
    date_added = Column(Date, default=date.today())


def create_db():
    Base.metadata.drop_all(db_engine)
    Base.metadata.create_all(db_engine)
