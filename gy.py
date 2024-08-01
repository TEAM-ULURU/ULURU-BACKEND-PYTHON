from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

# 새로운 데이터 모델 정의
class BACRequest(BaseModel):
    alcohol_volume_ml: float  # 알코올 음료의 양 (ml)
    alcohol_percentage: float  # 알코올 음료의 도수 (%)
    body_weight_kg: float  # 체중 (kg)
    gender: str = Field(..., pattern="^(male|female)$")  # 성별 ("male" 또는 "female")

# BAC 계산 함수
def calculate_bac(alcohol_volume_ml: float, alcohol_percentage: float, body_weight_kg: float, gender: str) -> float:
    # 성별에 따른 R 값 설정
    r = 0.68 if gender == "male" else 0.55
    
    # 섭취한 알코올의 양 (g) 계산
    alcohol_consumed = alcohol_volume_ml * (alcohol_percentage / 100) * 0.7894
    
    # BAC 계산
    bac = (alcohol_consumed / (body_weight_kg * r)) / 10  # BAC는 mg/10 = %
    return max(bac, 0)  # BAC는 음수일 수 없으므로 최소값을 0으로 설정

# 엔드포인트 정의
@app.post("/api/calculate-bac")
def get_bac(data: BACRequest):
    bac = calculate_bac(
        alcohol_volume_ml=data.alcohol_volume_ml,
        alcohol_percentage=data.alcohol_percentage,
        body_weight_kg=data.body_weight_kg,
        gender=data.gender
    )
    return {"bac": round(bac, 4)}

@app.get("/")
def read_root():
    return {"message": "Welcome to the BAC Calculator API!"}
