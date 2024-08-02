from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from database import Base

# Member 모델 정의
class Member(Base):
    __tablename__ = 'member'
    id = Column(Integer, primary_key=True, index=True)
    gender = Column(String, nullable=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    body_fat_percentage = Column(Float, nullable=True)

    #drink information
    drinking_frequency_reference_value = Column(String, nullable=True)
    drinking_frequency = Column(Float, nullable=True)
    type_of_alcohol = Column(String, nullable=True)  # Enum 제거
    average_alcohol_intake = Column(String, nullable=True)
    number_of_bottles = Column(Float, nullable=True)
    degree_of_intoxication = Column(String, nullable=True)
    percent_per_reference_value = Column(Float, nullable=True)

    #etc
    emergency_contact = Column(String, nullable=True)
    street_name_address = Column(String, nullable=True)
    detail_address = Column(String, nullable=True)

    is_oauth = Column(Boolean, nullable=True)

    calendar_id = Column(Integer, ForeignKey('calendar.id'), nullable=True)
    calendar = relationship("Calendar", back_populates="members")

    room_id = Column(Integer, ForeignKey('room.id'), nullable=True)
    room = relationship("Room", back_populates="members")

    member_friends = relationship("MemberFriend", foreign_keys="[MemberFriend.member_id]", back_populates="member")
    friends = relationship("MemberFriend", foreign_keys="[MemberFriend.friend_id]", back_populates="friend")


# Room 모델 정의
class Room(Base):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True, index=True)
    room_code = Column(String, nullable=True)
    members = relationship("Member", back_populates="room")


# Calendar 모델 정의
class Calendar(Base):
    __tablename__ = 'calendar'

    id = Column(Integer, primary_key=True, index=True)
    members = relationship("Member", back_populates="calendar")


# MemberFriend 모델 정의
class MemberFriend(Base):
    __tablename__ = 'member_friend'

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey('member.id'))
    friend_id = Column(Integer, ForeignKey('member.id'))
    member = relationship("Member", foreign_keys=[member_id], back_populates="member_friends")
    friend = relationship("Member", foreign_keys=[friend_id])
