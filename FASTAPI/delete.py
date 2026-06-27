from pydantic import BaseModel, Field, computed_field
from fastapi import FastAPI, HTTPException
import json
from typing import Optional, List, Dict, Annotated, Literal
from fastapi.responses import JSONResponse
from POST import Patient

app = FastAPI()

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(None, description="The name of the patient", example="John Doe")]
    city: Annotated[Optional[str], Field(None, description="The city of the patient", example="New York")]
    age: Annotated[Optional[int], Field(None, description="The age of the patient", gt=0, lt=120, example="30")]
    gender: Annotated[Optional[Literal["male", "female", "other"]], Field(None, description="The gender of the patient", example="male")]
    height: Annotated[Optional[float], Field(None, description="The height of the patient in meters", gt=0, example="1.75")]
    weight: Annotated[Optional[float], Field(None, description="The weight of the patient in kilograms", gt=0, example="70.5")]
    

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: str, patient: PatientUpdate):
    try:
        with open("patients.json", "r") as f:
            patients = json.load(f)
            
        if patient_id not in patients:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        del patients[patient_id]
            
        with open("patients.json", "w") as f:
            json.dump(patients, f)
            
        response = {"message": "Patient deleted successfully"}
        return JSONResponse(content=response, status_code=200)
        
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))