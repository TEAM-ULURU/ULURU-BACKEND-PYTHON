from enum import Enum

from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

# class AlcoholType(str, Enum):
#     SOJU = "SOJU"
#     BEER = "BEER"
#     ETC = "ETC"

# Member Pydantic model
class MemberBase(BaseModel):
    gender: Optional[str] = None
    name: str
    age: int
    height: float
    weight: float
    body_fat_percentage: Optional[float] = None
    #email: str

    # Drink information
    drinking_frequency_reference_value: Optional[str] = None
    drinking_frequency: Optional[float] = None
    type_of_alcohol: Optional[str] = None #enum 제거
    average_alcohol_intake: Optional[str] = None
    number_of_bottles: Optional[float] = None
    degree_of_intoxication: Optional[str] = None
    percent_per_reference_value: Optional[float] = None

    number_of_drinks: Optional[int] = None

    # Etc
    emergency_contact: Optional[str] = None
    street_name_address: Optional[str] = None
    detail_address: Optional[str] = None

    is_oauth: Optional[bool] = None

    calendar_id: Optional[int] = None
    room_id: Optional[int] = None


class MemberCreate(MemberBase):
    # email: EmailStr
    pass

class MemberUpdate(MemberBase):
    pass


class Member(MemberBase):
    member_id: int

    class Config:
        orm_mode = True

#
# class Member(MemberInDBBase):
#     pass


# class MemberFriendBase(BaseModel):
#     number_of_drinking_together: int
#     member_id: int
#     friend_id: int
#
#
# class MemberFriendCreate(MemberFriendBase):
#     pass
#
#
# class MemberFriendUpdate(MemberFriendBase):
#     pass
#
#
# class MemberFriendInDBBase(MemberFriendBase):
#     id: int
#
#     class Config:
#         orm_mode = True
#
#
# class MemberFriend(MemberFriendInDBBase):
#     pass


class RoomBase(BaseModel):
    room_code: Optional[str] = None


class RoomCreate(RoomBase):
    pass


class RoomUpdate(RoomBase):
    pass


class RoomInDBBase(RoomBase):
    id: int
    members: List[Member] = []

    class Config:
        orm_mode = True


class Room(RoomInDBBase):
    pass


# class CalendarBase(BaseModel):
#     pass
#
#
# class CalendarCreate(CalendarBase):
#     pass
#
#
# class CalendarUpdate(CalendarBase):
#     pass
#
#
# class CalendarInDBBase(CalendarBase):
#     id: int
#     members: List[Member] = []
#
#     class Config:
#         orm_mode = True
#
#
# class Calendar(CalendarInDBBase):
#     pass
