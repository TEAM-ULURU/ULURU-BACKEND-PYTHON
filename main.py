from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal, engine, Base
from models import User as UserModel, DrinkingHabits as DrinkingHabitsModel
from schemas import User, UserCreate, DrinkingHabits, DrinkingHabitsCreate


# SQLAlchemy 테이블 생성
Base.metadata.create_all(bind=engine)

# branch test lgy

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserModel(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users

@app.post("/drinking_habits/", response_model=DrinkingHabits)
def create_drinking_habit(drinking_habit: DrinkingHabitsCreate, db: Session = Depends(get_db)):
    db_drinking_habit = DrinkingHabitsModel(**drinking_habit.dict())
    db.add(db_drinking_habit)
    db.commit()
    db.refresh(db_drinking_habit)
    return db_drinking_habit

@app.get("/drinking_habits/", response_model=List[DrinkingHabits])
def read_drinking_habits(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    drinking_habits = db.query(DrinkingHabitsModel).offset(skip).limit(limit).all()
    return drinking_habits
