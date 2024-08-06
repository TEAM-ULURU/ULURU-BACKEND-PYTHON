import json

import jwt
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import SessionLocal, engine, Base
from models import Member as MemberModel, Room as RoomModel #Calendar as CalendarModel #MemberFriend as MemberFriendModel
from schemas import *

# # 데이터베이스 초기화
# Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://alt-web.run.goorm.io/entering-page-1"],  # React 앱의 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 의존성 주입 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 토큰 디코딩 함수
def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_ACCESS_SECRET, algorithms=[settings.ALGORITHM])
        #print(payload)
        return payload.get("member_id")
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


# Member 저장 API
@app.post("/save_members/", response_model=Member)
def create_member(member: MemberCreate, token: str = Query(...), db: Session = Depends(get_db)):
    #print("start decode")
    member_id = decode_token(token)
    print(member_id)
    #member_id = 1
    if not member_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    db_member = db.query(MemberModel).filter(MemberModel.member_id == member_id).first()
    #print(db_member)
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    for key, value in vars(member).items():
        if value is not None:
            setattr(db_member, key, value)
    db.commit()
    db.refresh(db_member)
    return db_member

# Member 저장 API - 토큰 넘기는 방식 헤더부분으로
@app.post("/save_members_header/", response_model=Member)
def create_member(member: MemberCreate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    #print("start decode")
    member_id = decode_token(token)
    print(member_id)
    #member_id = 1
    if not member_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    db_member = db.query(MemberModel).filter(MemberModel.member_id == member_id).first()
    #print(db_member)
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    for key, value in vars(member).items():
        if value is not None:
            setattr(db_member, key, value)
    db.commit()
    db.refresh(db_member)
    return db_member

# drinking_date 저장 API
@app.post("/save_date/", response_model=Member)
def save_date(member: MemberCreate, token: str = Query(...), db: Session = Depends(get_db)):
    # print("start decode")
    member_id = decode_token(token)
    print(member_id)
    # member_id = 1
    if not member_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    db_member = db.query(MemberModel).filter(MemberModel.member_id == member_id).first()
    db_member.drinking_date = member.drinking_date
    # print(db_member)
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    db.commit()
    db.refresh(db_member)
    return db_member

# Room 생성 API
@app.post("/rooms/", response_model=Room)
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    db_room = RoomModel(**room.dict(exclude_unset=True))
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

# # Calendar 생성 엔드포인트
# @app.post("/calendars/", response_model=Calendar)
# def create_calendar(calendar: CalendarCreate, db: Session = Depends(get_db)):
#     db_calendar = CalendarModel(**calendar.dict(exclude_unset=True))
#     db.add(db_calendar)
#     db.commit()
#     db.refresh(db_calendar)
#     return db_calendar

# # MemberFriend 생성 엔드포인트
# @app.post("/member_friends/", response_model=MemberFriend)
# def create_member_friend(member_friend: MemberFriendCreate, db: Session = Depends(get_db)):
#     db_member_friend = MemberFriendModel(**member_friend.dict(exclude_unset=True))
#     db.add(db_member_friend)
#     db.commit()
#     db.refresh(db_member_friend)
#     return db_member_friend

# 혈중알코올농도 API
@app.get("/BAC/{member_id}")
def read_member(member_id: int, db: Session = Depends(get_db)):
    db_member = db.query(MemberModel).filter(MemberModel.member_id == member_id).first()
    print(db_member)
    # 성별에 따른 R 값 설정
    r = 0.68 if db_member.gender == "Male" else 0.55
    print(r)
    # 섭취한 술의 양
    alcohol_volume_beer = db_member.now_beer_ml * db_member.now_drink_beer
    alcohol_volume_soju = db_member.now_soju_ml * db_member.now_drink_soju

    # 섭취한 알코올의 양 (g) 계산
    alcohol_beer = alcohol_volume_beer * (5 / 100) * 0.7894
    alcohol_soju = alcohol_volume_soju * (16 / 100) * 0.7894

    alcohol_consumed = alcohol_beer + alcohol_soju

    # BAC 계산
    bac = round((alcohol_consumed / (db_member.weight * r)) / 10, 2)  # BAC는 mg/10 = %
    print(bac)
    # DB에 저장
    db_member.current_blood_alcohol_level = bac
    db.commit()
    db.refresh(db_member)

    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")

    return db_member.current_blood_alcohol_level


# 취한 정도 API
@app.get("/intoxication/{member_id}")
def read_member(member_id: int, db: Session = Depends(get_db)):
    db_member = db.query(MemberModel).filter(MemberModel.member_id == member_id).first()
    # 취한 정도 계산
    i = ((db_member.current_blood_alcohol_level - 0.02) / (0.31-0.02)) * 95 + 5

    # DB에 저장
    db_member.current_level_of_intoxication = i
    db.commit()
    db.refresh(db_member)

    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")

    return db_member.current_level_of_intoxication


# # calendar_info API
# @app.get("/calendar_info/{member_id}", response_model=Member)
# def read_member(member_id: int, db: Session = Depends(get_db)):
#     calendar_info = dict()
#     db_member = db.query(MemberModel).filter(MemberModel.member_id == member_id).first()
#     calendar_info[db_member.drinking_date] = [db_member.current_blood_alcohol_level, db_member.current_level_of_intoxication]
#     print(calendar_info)
#     # DB에 저장
#     db_member.calendar_info = json.dumps(calendar_info)
#     print(db_member.calendar_info)
#     db.commit()
#     db.refresh(db_member)
#     if db_member is None:
#         raise HTTPException(status_code=404, detail="Member not found")
#     return db_member.calendar_info

# member 데이터 가져오는 api
@app.get("/member_info/{member_id}", response_model=Member)
def read_member(member_id: int, db: Session = Depends(get_db)):
    db_member = db.query(MemberModel).filter(MemberModel.member_id == member_id).first()
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


@app.get("/get_payload/{token}")
def get_payload_info(token: str):
    member_id = decode_token(token)
    if not member_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    return member_id


# # Calendar 읽기 엔드포인트
# @app.get("/calendars/{calendar_id}", response_model=Calendar)
# def read_calendar(calendar_id: int, db: Session = Depends(get_db)):
#     db_calendar = db.query(CalendarModel).filter(CalendarModel.id == calendar_id).first()
#     if db_calendar is None:
#         raise HTTPException(status_code=404, detail="Calendar not found")
#     return db_calendar

# # MemberFriend 읽기 엔드포인트
# @app.get("/member_friends/{member_friend_id}", response_model=MemberFriend)
# def read_member_friend(member_friend_id: int, db: Session = Depends(get_db)):
#     db_member_friend = db.query(MemberFriendModel).filter(MemberFriendModel.id == member_friend_id).first()
#     if db_member_friend is None:
#         raise HTTPException(status_code=404, detail="MemberFriend not found")
#     return db_member_friend
