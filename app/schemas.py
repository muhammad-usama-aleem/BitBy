import enum
from pydantic import BaseModel


class User(BaseModel):
    # id: int
    secret: str
    master: bool
    # leverage_type: enum
    leverage_value: float
    # master_id: int

    class Config():
        orm_mode = True


class ShowUser(BaseModel):
    secret: str
    master: bool
    # leverage_type: enum
    leverage_value: float
    id: int

    class Config():
        orm_mode = True


class Child(BaseModel):
    id: int
    secret: str
    master: bool
    leverage_type: str
    leverage_value: float
    master_id: int

    class Config():
        orm_mode = True