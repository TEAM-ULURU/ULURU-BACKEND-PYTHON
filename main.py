from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Member as MemberModel, Room as RoomModel, Calendar as CalendarModel, MemberFriend as MemberFriendModel
from schemas import *

# 데이터베이스 초기화
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 의존성 주입 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Member 생성 엔드포인트
@app.post("/members/", response_model=Member)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    db_member = MemberModel(**member.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

# Room 생성 엔드포인트
@app.post("/rooms/", response_model=Room)
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    db_room = RoomModel(**room.dict(exclude_unset=True))
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

# Calendar 생성 엔드포인트
@app.post("/calendars/", response_model=Calendar)
def create_calendar(calendar: CalendarCreate, db: Session = Depends(get_db)):
    db_calendar = CalendarModel(**calendar.dict(exclude_unset=True))
    db.add(db_calendar)
    db.commit()
    db.refresh(db_calendar)
    return db_calendar

# MemberFriend 생성 엔드포인트
@app.post("/member_friends/", response_model=MemberFriend)
def create_member_friend(member_friend: MemberFriendCreate, db: Session = Depends(get_db)):
    db_member_friend = MemberFriendModel(**member_friend.dict(exclude_unset=True))
    db.add(db_member_friend)
    db.commit()
    db.refresh(db_member_friend)
    return db_member_friend

# Member 읽기 엔드포인트
@app.get("/members/{member_id}", response_model=Member)
def read_member(member_id: int, db: Session = Depends(get_db)):
    db_member = db.query(MemberModel).filter(MemberModel.id == member_id).first()
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_member

# Room 읽기 엔드포인트
@app.get("/rooms/{room_id}", response_model=Room)
def read_room(room_id: int, db: Session = Depends(get_db)):
    db_room = db.query(RoomModel).filter(RoomModel.id == room_id).first()
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room

# Calendar 읽기 엔드포인트
@app.get("/calendars/{calendar_id}", response_model=Calendar)
def read_calendar(calendar_id: int, db: Session = Depends(get_db)):
    db_calendar = db.query(CalendarModel).filter(CalendarModel.id == calendar_id).first()
    if db_calendar is None:
        raise HTTPException(status_code=404, detail="Calendar not found")
    return db_calendar

# MemberFriend 읽기 엔드포인트
@app.get("/member_friends/{member_friend_id}", response_model=MemberFriend)
def read_member_friend(member_friend_id: int, db: Session = Depends(get_db)):
    db_member_friend = db.query(MemberFriendModel).filter(MemberFriendModel.id == member_friend_id).first()
    if db_member_friend is None:
        raise HTTPException(status_code=404, detail="MemberFriend not found")
    return db_member_friend
