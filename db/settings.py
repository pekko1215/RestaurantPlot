from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

DATABASE = 'sqlite:///./system.db'
ENGINE = create_engine(
    DATABASE,
    encoding = 'utf-8',
    echo=True
)

DBSession = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind = ENGINE
))

Base = declarative_base()
Base.query = DBSession.query_property()