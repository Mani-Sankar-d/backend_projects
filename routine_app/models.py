from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__='users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    routines = relationship('Routine', back_populates='user')

class Routine(Base):
    __tablename__='routines'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String, nullable=True)
    date = Column(Date)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='routines')
