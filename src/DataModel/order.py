from ast import For
from sqlalchemy.orm import declarative_base
from sqlalchemy import BOOLEAN, Column, Integer, String, ForeignKey,DateTime,Enum
from datetime import datetime


Base= declarative_base()


class coin_deposit(Base):
    __tablename__ = 'coin_deposit'
    id = Column(Integer(),unique=True,primary_key=True,autoincrement=True)
    deposit = Column(Integer())
    deposit_order = Column(Integer())
    deposit_count=Column(Integer())
    
    
    def __repr__(self):
        return f">>>>>  user_id : {self.id}  deposit : {self.deposit} deposit_order : {self.deposit_order} deposit_count: {self.deposit_count}"
    