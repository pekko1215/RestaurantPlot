import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from .settings import Base
from .settings import ENGINE

class User(Base):
    """
    ユーザモデル
    """
    __tablename__ = 'users'
    id = Column('id', String(32), primary_key = True)
    name = Column('name', String(200))

def main(args):
    """
    メイン関数
    呼び出すとテーブルの作成を行う
    """
    Base.metadata.create_all(bind=ENGINE)

if __name__ == "__main__":
    main(sys.argv)