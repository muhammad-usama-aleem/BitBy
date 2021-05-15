from sqlalchemy import Column, Integer, String, Boolean, Float
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    # apikey = Column(String)
    secret = Column(String)
    master = Column(Boolean)
    # leverage_value = Column(Float)
    #master_id = Column(Integer)


class Child(Base):
    __tablename__ = 'child'

    id = Column(Integer, primary_key=True, index=True)
    # apikey = Column(String)
    secret = Column(String)
    master = Column(Boolean)
    leverage_type = Column(String)#added lverage type
    leverage_value = Column(Float)
    master_id = Column(Integer)