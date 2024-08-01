from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID


class MemberFriendBase(BaseModel):
    member_id: int
    friend_id: int

class MemberFriendCreate(MemberFriendBase):
    pass

class MemberFriend(MemberFriendBase):
    id: int

    class Config:
        orm_mode = True

class CalendarBase(BaseModel):
    pass

class CalendarCreate(CalendarBase):
    pass

class Calendar(CalendarBase):
    id: int

    class Config:
        orm_mode = True

class RoomBase(BaseModel):
    room_code: str

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    id: int
    members: List[int]

    class Config:
        orm_mode = True

class MemberBase(BaseModel):
    gender: Optional[str] = None
    name: str
    age: int
    height: float
    weight: float
    body_fat_percentage: Optional[float] = None
    drinking_frequency_reference_value: Optional[float] = None
    drinking_frequency: Optional[float] = None
    type_of_alcohol: Optional[str] = None
    average_alcohol_intake: Optional[float] = None
    degree_of_intoxication: Optional[float] = None
    emergency_contact: Optional[str] = None
    is_oauth: Optional[bool] = None
    calendar_id: Optional[int] = None
    room_id: Optional[int] = None

class MemberCreate(MemberBase):
    pass

class Member(MemberBase):
    id: int

    class Config:
        orm_mode = True
