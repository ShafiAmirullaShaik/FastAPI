import json

from pydantic import BaseModel, Field, computed_field
from typing import Optional, List, Dict, Annotated, Literal
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(title="Patient API", description="API for managing patient data", version="1.0.0")

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="The unique identifier for the patient", example="P001")]
    name: Annotated[str, Field(..., description="The name of the patient", example="John Doe")]
    city: Annotated[str, Field(..., description="The city of the patient", example="New York")]
    age: Annotated[int, Field(..., description="The age of the patient", gt=0, lt=120, example="30")]
    gender: Annotated[Literal["male", "female", "other"], Field(..., description="The gender of the patient", example="male")]
    height: Annotated[float, Field(..., description="The height of the patient in meters", gt=0, example="1.75")]
    weight: Annotated[float, Field(..., description="The weight of the patient in kilograms", gt=0, example="70.5")]
    
    @computed_field
    @property
    def bmi(self) -> float:
        """Calculate the Body Mass Index (BMI) of the patient."""
        return round(self.weight / (self.height ** 2), 2)
    
    @computed_field
    @property
    def bmi_category(self) -> str:
        """Determine the BMI category of the patient."""
        bmi_value = self.bmi
        if bmi_value < 18.5:
            return "Underweight"
        elif 18.5 <= bmi_value < 24.9:
            return "Normal weight"
        elif 25 <= bmi_value < 29.9:
            return "Overweight"
        else:
            return "Obesity"
        
def load_data() -> List[Dict]:
    """Load existing patient data from a JSON file."""
    try:
        with open("patients.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
        
@app.post("/create_patient")
def create_patient(patient: Patient):
    """
    Create a new patient record.

    - **id**: Unique identifier for the patient (e.g., "P001")
    - **name**: Name of the patient (e.g., "John Doe")
    - **city**: City of the patient (e.g., "New York")
    - **age**: Age of the patient (must be between 1 and 119)
    - **gender**: Gender of the patient (must be "male", "female", or "other")
    - **height**: Height of the patient in meters (must be greater than 0)
    - **weight**: Weight of the patient in kilograms (must be greater than 0)
    """
    
    ## Load Exisiting Date
    data = load_data()
    
    ## Check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail=f"Patient with ID {patient.id} already exists.")
    
    ## New Patient Creation
    data[patient.id] = patient.model_dump(exclude=['id'])
    
    ## Save the updated data back to the JSON file
    with open("patients.json", "w") as file:
        json.dump(data, file)
        
    return JSONResponse(status_code=201, content={"message": f"Patient with ID {patient.id} created successfully."})