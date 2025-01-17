from enum import Enum

from pydantic import BaseModel, Field, EmailStr, json
from typing import List, Optional, Dict

# class AlcoholType(str, Enum):
#     SOJU = "SOJU"
#     BEER = "BEER"
#     ETC = "ETC"

class CalendarDate(BaseModel):
    member_id: int
    drinking_date: Optional[str] = None

    class Config:
        orm_mode = True



# Member Pydantic model
class MemberBase(BaseModel):
    gender: Optional[str] = None
    name: str = None
    age: int = None
    height: float = None
    weight: float = None
    body_fat_percentage: Optional[float] = None
    #email: str
    calendar_info: Optional[dict] = None

    # Drink information
    drinking_date: Optional[str] = None
    drinking_frequency_reference_value: Optional[str] = None
    drinking_frequency: Optional[float] = None
    type_of_alcohol: Optional[str] = None #enum 제거
    average_alcohol_intake: Optional[str] = None
    number_of_bottles: Optional[float] = None
    degree_of_intoxication: Optional[str] = None
    percent_per_reference_value: Optional[float] = None
    number_of_drinks: Optional[int] = None

    current_level_of_intoxication: Optional[float] = None
    current_blood_alcohol_level: Optional[float] = None

    now_beer_ml: Optional[float] = None
    now_drink_beer: Optional[float] = None
    now_soju_ml: Optional[float] = None
    now_drink_soju: Optional[float] = None

    # Etc
    emergency_contact: Optional[str] = None
    street_name_address: Optional[str] = None
    detail_address: Optional[str] = None

    is_oauth: Optional[int] = None

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
