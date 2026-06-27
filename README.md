# FastAPI Patient Management API

A simple patient management API built with FastAPI and Pydantic. This repository includes endpoints for creating, reading, updating, and deleting patient records stored locally in `FASTAPI/patients.json`.

## Features
- Create new patient records
- Retrieve all patients or a specific patient by ID
- Update patient records with partial updates
- Delete existing patient records
- Pydantic validation for patient fields
- Computed BMI and BMI category properties

## Technologies Used
- Python
- FastAPI
- Pydantic
- Uvicorn

## Setup
1. Activate the virtual environment:
   - PowerShell:
     ```powershell
     .\myenv\Scripts\Activate.ps1
     ```
   - Command Prompt:
     ```bat
     .\myenv\Scripts\activate.bat
     ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the FastAPI application:
   ```bash
   uvicorn FASTAPI.patientapp:app --reload
   ```

## API Files
- `FASTAPI/POST.py` - Patient creation endpoint and Pydantic `Patient` model
- `FASTAPI/put.py` - Patient update endpoint with optional `PatientUpdate` fields
- `FASTAPI/PUT&DELETE.py` - Alternate update/delete implementation
- `FASTAPI/GET.py` - Read-only retrieval endpoints
- `FASTAPI/patient_models.py` - Pydantic model examples and validation helpers
- `FASTAPI/patients.json` - Sample patient data storage file

## Usage
- Create a patient: `POST /create_patient`
- Update a patient: `PUT /patients/{patient_id}`
- Delete a patient: `DELETE /patients/{patient_id}`
- Get all patients: `GET /patients`
- Get a patient by ID: `GET /patients/{patient_id}`

## Notes
- The project stores data locally in `FASTAPI/patients.json`.
- Use the FastAPI docs UI at `http://127.0.0.1:8000/docs` after starting the server.
