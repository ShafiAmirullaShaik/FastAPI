from fastapi import FastAPI, Path, HTTPException, Query

app = FastAPI()

patients = [
    {
        'ID': 'P001',
        'name': 'John Doe',
        'age': 30,
        'diagnosis': 'Flu'
    },
    {
        'ID': 'P002',
        'name': 'Jane Smith',
        'age': 25,
        'diagnosis': 'Cold'
    }
]

# Endpoint to add a new patient
@app.post("/add")
def add_patient(patient_id: str, name: str, age: int, diagnosis: str):
    new_patient = {
        'ID': patient_id,
        'name': name,
        'age': age,
        'diagnosis': diagnosis
    }
    patients.append(new_patient)
    return {"message": "Patient added successfully.", "patient": new_patient}

# Endpoint to view all patients
@app.get("/view")
def view_patients():
    return {"patients": patients}

# Endpoint to view a specific patient by ID
@app.get("/")
def read_root():
    message = "Welcome to the Patient Management API!"
    return {"notification": message}

# Endpoint to provide information about the API
@app.get("/about")
def read_about():
    message = "This API allows you to manage patient records. You can add new patients, view existing patients, update patient information, and delete patient records."
    return {"about": message}

# Endpoint to view a specific patient by ID
@app.get("/view/{patient_id}")
def view_patient(patient_id: str = Path(..., description="The ID of the patient to view", example="P001")):
    patient = next((p for p in patients if p['ID'] == patient_id), None)
    if patient:
        return {"patient": patient}
    else:
        raise HTTPException(status_code=404, detail="Patient not found.")

# Endpoint to update patient information
@app.put("/update/{patient_id}")
def update_patient(patient_id: str = Path(..., description="The ID of the patient to update", example="P001"), name: str = None, age: int = None, diagnosis: str = None):
    patient = next((p for p in patients if p['ID'] == patient_id), None)
    if patient:
        if name:
            patient['name'] = name
        if age:
            patient['age'] = age
        if diagnosis:
            patient['diagnosis'] = diagnosis
        return {"message": "Patient updated successfully.", "patient": patient}
    else:
        raise HTTPException(status_code=404, detail="Patient not found.")

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str = Path(..., description="The ID of the patient to delete", example="P001")):
    global patients
    patients = [p for p in patients if p['ID'] != patient_id]
    return {"message" : f"Patient with ID {patient_id} deleted successfully."}

# Endpoint to sort patients by a specified field and order
@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="The field to sort patients by (name, age, diagnosis)"), order: str = Query("asc", description="The sort order (asc or desc)")):
    if sort_by not in ["name", "age", "diagnosis"]:
        raise HTTPException(status_code=400, detail="Invalid sort field. Must be 'name', 'age', or 'diagnosis'.")

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid sort order. Must be 'asc' or 'desc'.")
    
    sorted_patients = sorted(patients, key=lambda x: x[sort_by], reverse=(order == "desc"))
    return {"sorted_patients": sorted_patients}