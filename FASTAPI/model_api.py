from pydantic import BaseModel, Field, computed_field
from fastapi import FastAPI, HTTPException
from typing import Optional, List, Dict, Annotated, Literal
from fastapi.responses import JSONResponse
import pandas
import pickle

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

class User(BaseModel):
    age: Annotated[int, Field(..., description="The age of the user", gt=0, lt=120, example="30")]
    weight: Annotated[float, Field(..., description="The weight of the user in kilograms", gt=0, example="70.5")]
    height: Annotated[float, Field(..., description="The height of the user in meters", gt=0, example="1.75")]
    income_lpa: Annotated[float, Field(..., description="The income of the user in LPA", gt=0, example="10.45")]
    smoker: Annotated[bool, Field(..., description="Whether the user smokes")]
    city: Annotated[str, Field(..., description="The city of the user", example="Hyderabad")]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'], Field(..., description="The occupation of the user", example="retired")]
    
    @computed_field
    def bmi(self) -> float:
        """Calculate the Body Mass Index (BMI) of the patient."""
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    def lifestyle_risk(self) -> str:
        if self.bmi > 30 and self.smoker:
            return 'high'
        elif self.bmi > 27 or self.smoker:
            return 'medium'
        else:
            return 'low'

    @computed_field
    def age_group(self) -> str:
        if self.age < 25:
            return 'young'
        elif 25 <= self.age < 45:
            return 'adult'
        elif self.age >= 45 and self.age < 65:
            return 'middle-aged'
        else:
            return 'senior'

    @computed_field
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3

app = FastAPI()

@app.post("/predict")
def predict(user: User):
    try:
        df = pandas.DataFrame([
            {
                'bmi': user.bmi,
                'lifestyle_risk': user.lifestyle_risk,
                'age_group': user.age_group,
                'city_tier': user.city_tier,
                'income_lpa': user.income_lpa,
                'smoker': user.smoker,
                'occupation': user.occupation
            }
        ])
        print('-----------------')
        print(model.predict(df))
        print('-----------------')

        prediction = model.predict(df)[0]
        return JSONResponse(status_code=200, content={"prediction": prediction})
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    