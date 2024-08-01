from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, validator
from typing import Optional
import re

app = FastAPI()

# bac-develop

class UserSurvey(BaseModel):
    gender: str = Field(..., pattern="^(male|female)$")
    age: int = Field(..., gt=18, lt=120)
    height: int = Field(..., gt=100, lt=250)
    weight: int = Field(..., gt=20, lt=300)
    body_fat: Optional[float] = Field(None, gt=0)
    drinking_frequency_basis: str = Field(..., pattern="^(1개월 기준|1주일 기준|2주일 기준|1일 기준)$")
    drinking_frequency: int = Field(..., gt=0)
    preferred_drink: str = Field(..., pattern="^(소주|맥주)$")
    average_drinking_basis: str = Field(..., pattern="^(1시간 기준|2시간 기준|3시간 기준|4시간 기준)$")
    average_drinking_bottles: int = Field(..., gt=0)
    intoxication_basis: str = Field(..., pattern="^(1병 기준|2병 기준|3병 기준|4병 기준)$")
    intoxication_percent: float = Field(..., gt=0)
    address: str
    detailed_address: str
    emergency_contact: str

    @validator('emergency_contact')
    def validate_emergency_contact(cls, v):
        if not re.match(r'^010-\d{4}-\d{4}$', v):
            raise ValueError('emergency_contact must be in the format 010-0000-0000')
        return v

class DrinkInfo(BaseModel):
    drink_type: str = Field(..., pattern="^(소주|맥주)$")
    drink_count: int = Field(..., gt=0)
    alcohol_content: float = Field(..., gt=0)  # 알코올 농도(%)

@app.post("/survey/")
async def submit_survey(survey: UserSurvey, drink_info: DrinkInfo):
    # 혈중알코올농도 계산 로직
    bac = calculate_bac(survey, drink_info)
    return {"bac": bac}

def calculate_bac(survey: UserSurvey, drink_info: DrinkInfo) -> float:
    # 사용자의 체중과 성별을 입력받아야 합니다.
    weight_kg = survey.weight  # 사용자의 체중
    gender = survey.gender  # 사용자의 성별
    
    # 성별에 따른 알코올 분포 계수 설정
    if gender == "male":
        r = 0.68
    else:
        r = 0.55
    
    # 음주량 (ml)을 계산
    if drink_info.drink_type == "소주":
        volume_per_drink = 50  # 소주 기본 용량 (ml)
    elif drink_info.drink_type == "맥주":
        volume_per_drink = 225  # 맥주 기본 용량 (ml)
    else:
        raise HTTPException(status_code=400, detail="Invalid drink type")
    
    total_alcohol_ml = volume_per_drink * drink_info.drink_count * (drink_info.alcohol_content / 100) * 0.7894
    
    # 혈중 알코올 농도 계산
    bac = (total_alcohol_ml / (weight_kg * r)) / 10
    return bac

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

