import enum

from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base

# class AlcoholType(enum.Enum):
#     SOJU = "SOJU"
#     BEER = "BEER"
#     ETC = "ETC"

# Member 모델 정의
class Member(Base):
    __tablename__ = 'member'
    member_id = Column(Integer, primary_key=True, index=True)
    gender = Column(String, nullable=True)
    name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    body_fat_percentage = Column(Float, nullable=True)
    current_level_of_intoxication = Column(Float, nullable=True)
    current_blood_alcohol_level = Column(Float, nullable=True)

    #email = Column(String, nullable=False)

    #drink information
    drinking_date = Column(String, nullable=True) # 캘린더 날짜 정보
    drinking_frequency_reference_value = Column(String, nullable=True)
    drinking_frequency = Column(Float, nullable=True)
    type_of_alcohol = Column(String, nullable=True) #enum 제거
    average_alcohol_intake = Column(String, nullable=True)
    number_of_bottles = Column(Float, nullable=True)
    degree_of_intoxication = Column(String, nullable=True)
    percent_per_reference_value = Column(Float, nullable=True)
    number_of_drinks = Column(Integer, nullable=True)

    now_beer_ml = Column(Float, nullable=True)
    now_drink_beer = Column(Float, nullable=True)
    now_soju_ml = Column(Float, nullable=True)
    now_drink_soju = Column(Float, nullable=True)

    #etc
    emergency_contact = Column(String, nullable=True)
    street_name_address = Column(String, nullable=True)
    detail_address = Column(String, nullable=True)

    is_oauth = Column(Boolean, nullable=True)

    # calendar_id = Column(Integer, ForeignKey('calendar.calendar_id'), nullable=True)
    # calendar = relationship("Calendar", back_populates="members")

    room_id = Column(Integer, ForeignKey('room.room_id'), nullable=True)
    room = relationship("Room", back_populates="members")

    # member_friend_id = Column(Integer, ForeignKey('member_friend.member_friend_id'), nullable=True)
    # member_friend = relationship("MemberFriend", back_populates="members")

# Room 모델 정의
class Room(Base):
    __tablename__ = 'room'

    room_id = Column(Integer, primary_key=True, index=True)
    room_code = Column(String, nullable=True)
    members = relationship("Member", back_populates="room")


# # Calendar 모델 정의
# class Calendar(Base):
#     __tablename__ = 'calendar'
#
#     calendar_id = Column(Integer, primary_key=True, index=True)
#     members = relationship("Member", back_populates="calendar")
#

# # MemberFriend 모델 정의
# class MemberFriend(Base):
#     __tablename__ = 'member_friend'
#     number_of_drinking_together = Column(Integer)
#     member_friend_id = Column(Integer, primary_key=True, index=True)
#     member_id = Column(Integer)
#     friend_id = Column(Integer)
#     members = relationship("Member", back_populates="member_friend")
