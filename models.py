from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()


# Enum 타입 정의
class TypeOfAlcohol(enum.Enum):
    BEER = "BEER"
    WINE = "WINE"
    SPIRITS = "SPIRITS"


# Member 모델 정의
class Member(Base):
    __tablename__ = 'member'

    id = Column(Integer, primary_key=True, autoincrement=True)
    gender = Column(String)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    body_fat_percentage = Column(Float)
    drinking_frequency_reference_value = Column(Float)
    drinking_frequency = Column(Float)
    type_of_alcohol = Column(Enum(TypeOfAlcohol))
    average_alcohol_intake = Column(Float)
    degree_of_intoxication = Column(Float)
    emergency_contact = Column(String)
    is_oauth = Column(Boolean)

    calendar_id = Column(Integer, ForeignKey('calendar.id'))
    calendar = relationship("Calendar", back_populates="member")

    room_id = Column(Integer, ForeignKey('room.id'))
    room = relationship("Room", back_populates="members")

    member_friends = relationship("MemberFriend", back_populates="member")

 #c
# Room 모델 정의
class Room(Base):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_code = Column(String)
    members = relationship("Member", back_populates="room")


# Calendar 모델 정의
class Calendar(Base):
    __tablename__ = 'calendar'

    id = Column(Integer, primary_key=True, autoincrement=True)
    member = relationship("Member", back_populates="calendar")


# MemberFriend 모델 정의
class MemberFriend(Base):
    __tablename__ = 'member_friend'

    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey('member.id'))
    friend_id = Column(Integer, ForeignKey('member.id'))
    member = relationship("Member", foreign_keys=[member_id], back_populates="member_friends")
    friend = relationship("Member", foreign_keys=[friend_id])

