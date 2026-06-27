# FastAPI Patient Management API

This repository contains a simple FastAPI project for managing patient records. It demonstrates basic API routes for creating, viewing, updating, deleting, and sorting patient data.

## Features
- Welcome and about endpoints
- Add new patients
- View all patients or a specific patient by ID
- Update patient information
- Delete a patient
- Sort patients by selected fields

## Technologies Used
- Python
- FastAPI
- Pydantic
- Uvicorn

## Getting Started
1. Create and activate a virtual environment
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   uvicorn FASTAPI.patientapp:app --reload
   ```

## Project Structure
- FASTAPI/patientapp.py - Main FastAPI application
- FASTAPI/patient_models.py - Pydantic models and validation examples
- FASTAPI/fastaapi.py - Basic FastAPI example
- requirements.txt - Python dependencies
