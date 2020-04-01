import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime,ForeignKey,REAL
from .settings import Base
from .settings import ENGINE
from . import user

class Restraurant(Base):
    """
    飲食店モデル
    """
    __tablename__ = 'restraurants'
    id = Column('id', Integer, primary_key = True,autoincrement=True)
    name = Column('name', String(200))
    comment = Column('comment',String(200))
    created_by = Column('created_by',ForeignKey('users.id'))
    x = Column('x',REAL)
    y = Column('y',REAL)
def main(args):
    """
    メイン関数
    呼び出すとテーブルの作成を行う
    """
    Base.metadata.create_all(bind=ENGINE)

if __name__ == "__main__":
    main(sys.argv)