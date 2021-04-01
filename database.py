from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text

db_path = "database/group.db"
Base = declarative_base()
engine = create_engine(f'sqlite:///{db_path}')

class Group_A(Base):
    __tablename__ = 'group_a'
    id = Column(Integer, primary_key = True)
    FIRSTFROMNAME = Column(String)
    LASTFROMNAME = Column(String)
    EMAIL = Column(String)
    EMAIL_PASS = Column(String)
    PROXY_PORT = Column(String)
    PROXY_USER = Column(String)
    PROXY_PASS = Column(String)

class Group_B(Base):
    __tablename__ = 'group_b'
    id = Column(Integer, primary_key = True)
    FIRSTFROMNAME = Column(String)
    LASTFROMNAME = Column(String)
    EMAIL = Column(String)
    EMAIL_PASS = Column(String)
    PROXY_PORT = Column(String)
    PROXY_USER = Column(String)
    PROXY_PASS = Column(String)


class Targets(Base):
    __tablename__ = 'targets'
    id = Column(Integer, primary_key = True)
    one = Column(String)
    two = Column(String)
    three = Column(String)
    TONAME = Column(String)
    EMAIL = Column(String)

Base.metadata.create_all(engine)
