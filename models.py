from database import Base
from sqlalchemy import Column,Integer,Boolean,Text,String,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType


class User(Base):
    __tablename__='user'
    id=Column(Integer,primary_key=True)
    username=Column(String(25),unique=True)
    email=Column(String(80),unique=True)
    password=Column(Text,nullable=True)
    is_staff=Column(Boolean,default=False)
    is_active=Column(Boolean,default=False)
    notes=relationship('Note',back_populates='user')


    def __repr__(self):
        return f"<User {self.username}"


class Note(Base):

    NOTE_STATUSES=(
        ('PENDING','pending'),
        ('IN-TRANSIT','in-transit'),
        ('DELIVERED','delivered')
    )

    __tablename__='notes'
    id=Column(Integer,primary_key=True)
    quantity=Column(Integer,nullable=False)
    note_status=Column(ChoiceType(choices=NOTE_STATUSES),default="PENDING")

    note_data=Column(Text, nullable = True)

    user_id=Column(Integer,ForeignKey('user.id'))
    user=relationship('User',back_populates='notes')

    def __repr__(self):
        return f"<Note {self.id}>"