from pydantic import BaseModel, ValidationError, Field, EmailStr, field_validator, model_validator, computed_field
from typing import Optional, List, Dict, Annotated
# ------------------------------
# Pydantic concepts explained:
# ------------------------------
# BaseModel: A data blueprint or form definition. It describes what data should look like.
#   Think of it as a template for a patient record. Pydantic uses it to check incoming data.
# Field(...): Marks a field as required and adds validation rules.
#   Example: Field(..., ge=0) is like saying "this number must be 0 or higher".
# Annotated: Attaches extra validation metadata to a type.
#   It is similar to writing a label on a form field with rules and instructions.
# EmailStr: A special string type that also checks email formatting.
#   It is like using a dedicated email field in a form rather than a plain text box.
# Optional[T]: Means the value can be either T or None.
#   It is like saying "this answer is optional" on a questionnaire.
# List[str], Dict[str, str]: Container types that validate their contents.
#   For example, List[str] ensures every item inside is a string.
# ValidationError: The error object Pydantic raises when input data is invalid.
#   It is like a report that explains why the submitted form was rejected.
#
# Type validation checks the basic shape of data (string, integer, list, dict).
# Data validation checks content rules (minimum values, string length, email format).
# Pydantic does both using the model and Field rules.
#
# field_validator: A decorator used for custom validation logic on one field.
#   It is like a second-level inspector for a single field after the basic checks.
#   Example:
#       @field_validator('email')
#       def validate_email(cls, value):
#           if not value.endswith('@example.com'):
#               raise ValueError('only example.com email allowed')
#           return value
#
# Overall analogy:
#   The Pydantic model is a mailbox with strict rules. Each field is a slot with its own size
#   and content requirements. If a package arrives wrong, Pydantic rejects it and returns details.
# class Patient(BaseModel):
#     name: str = Field(..., title="Name of the patient", max_length=100)
#     age: int = Field(..., ge=0, title="Age of the patient")

# class Patient(BaseModel):
#     name: str
#     age: int
#     weight: float
#     married: bool
#     allergies: List[str]
#     contnact_details: Dict[str, str]
class Address(BaseModel):
    # Nested model: an address is its own object with its own rules.
    # This is like a sub-form inside the patient form where address fields are grouped.
    street: str
    city: str
    state: str
    zip_code: str

class Patient(BaseModel):
    name: Annotated[str, Field(..., title="Name of the patient", max_length=100)]  # Name must be a string with a maximum length of 100 characters
    age: int = Field(..., ge=0, title="Age of the patient")  # Age must be a non-negative integer
    email: EmailStr
    weight: Annotated[float, Field(..., gt=0, title="Weight of the patient", strict=True)]  # Weight must be a positive float

    # Optional[float] with Field(None, ...) means the field is not required.
    # It is like an optional question on a form: if the user leaves it empty, that's allowed.
    height: Annotated[Optional[float], Field(None, gt=0, title="Height of the patient", strict=True)]  # Height must be a positive float if provided

    married: Annotated[Optional[bool], Field(None, title="Marital status of the patient")]  # Married must be a boolean value if present
    allergies: List[str]
    contnact_details: Dict[str, str]

    # Nested model validation: Pydantic will validate `address` using the Address model.
    # This means the patient’s address is not just a raw dict; it is a structured Address object.
    address: Address

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        # Field validator: validates one specific field after the basic type checks.
        # Think of it as a dedicated inspector who only checks the email field.
        valid_domains = ['gmail.com', 'yahoo.com', 'outlook.com']
        domain = v.split('@')[-1]
        if domain not in valid_domains:
            raise ValueError('Invalid email domain')
        return v
    
    @model_validator(mode='after')
    def validate_emergency_contact(self):
        # Model-level validator: runs after the entire model is created and validated.
        # This is like a final review of the whole form, checking rules that depend on multiple fields.
        if self.age > 60 and 'emergency_contact' not in self.contnact_details:
            raise ValueError('Emergency contact is required for patients over 60')
        return self
    
    @computed_field
    @property
    def bmi(self) -> Optional[float]:
        # Computed field: a value derived from other fields, not provided by input.
        # It is like a score calculated from the form answers.
        if self.weight and self.height:
            return round(self.weight / (self.height ** 2), 2)
        return None

## Issue with both insert_patient_date and update_patient_date functions is that they are not using Pydantic models for input validation. Instead, they are manually checking the types of the inputs AND validating them. This approach is not as robust or scalable as using Pydantic models, which provide automatic validation and serialization of input data.
# def insert_patient_date(name: str, age: int):
#     if type(name) is not str or type(age) is not int:
#         return {"error": "Invalid input types. Name must be a string and age must be an integer."}
#     elif age < 0:
#         return {"error": "Invalid age. Age must be a non-negative integer."}
#     else:
#         patient_data = {
#             "name": name,
#             "age": age
#         } 
#         return {"message": "Patient data inserted successfully.", "data": patient_data}

# def update_patient_date(name: str, age: int):
#     if type(name) is not str or type(age) is not int:
#         return {"error": "Invalid input types. Name must be a string and age must be an integer."}
#     elif age < 0:
#         return {"error": "Invalid age. Age must be a non-negative integer."}
#     else:
#         updated_data = {
#             "name": name,
#             "age": age
#         }
#         return {"message": "Patient data updated successfully.", "data": updated_data}
    
# if __name__ == "__main__": # __main__ is a special variable in Python that represents the name of the current module. When a Python script is run directly, the value of __name__ is set to "__main__". This allows us to include code that should only be executed when the script is run directly, and not when it is imported as a module in another script.
#     # Example usage of the functions
#     print(insert_patient_date("John Doe", 30))
#     print(update_patient_date("Jane Smith", 25))
    
#     print(insert_patient_date("Invalid Name", -5))  # Invalid age
#     print(update_patient_date(12345, 40))  # Invalid name type
    

## Now, let's implement the insert_patient_data and update_patient_data functions using Pydantic models for input validation.
# def insert_patient_data(patient: Patient):
#     try:
#         patient_name = patient.name  # Access the name field directly
#         patient_age = patient.age    # Access the age field directly
#         return {"message": "Patient data inserted successfully.", "data": {"name": patient_name, "age": patient_age}}
#     except ValidationError as e:
#         return {"error": e.errors()}

# patient_info = {
#     "name": "Alice Johnson",
#     "age": 28
# }
    
# patient = Patient(**patient_info)  # Create a Patient instance using the provided data
# print(insert_patient_data(patient))

# def update_patient_data(patient: Patient):
#     try:
#         patient_name = patient.name  # Access the name field directly
#         patient_age = patient.age    # Access the age field directly
#         return {"message": "Patient data updated successfully.", "data": {"name": patient_name, "age": patient_age}}
#     except ValidationError as e:
#         return {"error": e.errors()}

# patient_info_update = {
#     "name": "Bob Smith",
#     "age": 35
# }
    
# patient_update = Patient(**patient_info_update)  # Create a Patient instance using the provided data
# print(update_patient_data(patient_update))

def get_patient_data(patient: Patient):
    try:
        patient_name = patient.name  # Access the name field directly
        patient_age = patient.age    # Access the age field directly
        patient_email = patient.email
        patient_weight = patient.weight
        patient_married = patient.married
        patient_allergies = patient.allergies
        patient_contact_details = patient.contnact_details
        patient_address = patient.address
        print(f"Patient BMI: {patient.bmi}")  # Access the computed BMI property
        return {"message": "Patient data retrieved successfully.", "data": {"name": patient_name, "age": patient_age, "email": patient_email, "weight": patient_weight, "married": patient_married, "allergies": patient_allergies, "contact_details": patient_contact_details, "address": patient_address}}
    except ValidationError as e:
        return {"error": e.errors()}
    
address_info = {
    "street": "123 Main St",
    "city": "Anytown",
    "state": "CA",
    "zip_code": "12345"
}

address = Address(**address_info)  # Create a Patient instance using the provided data

patient_info = {
    "name": "Alice Johnson",
    "age": 80,
    "email": "shafi@yahoo.com",
    "weight": 65.5,
    "height": 1.7,
    "married": True,
    "allergies": ["dust", "pollen"],
    "contnact_details": {
        "phone": "123-456-7890",
        "emergency_contact": "987-654-3210"
    },
    "address": address_info
}

patient = Patient(**patient_info)  # Create a Patient instance using the provided data
print(get_patient_data(patient))

temp = patient.model_dump()  # Serialize the patient data to a dictionary
print(temp)
print(type(temp))  # Output: <class 'dict'>

temp1 = patient.model_dump_json()  # Serialize the patient data to a dictionary
print(temp1)
print(type(temp1))  # Output: <class 'dict'>

temp2 = patient.model_dump_json(exclude=['email', "age"])# Serialize the patient data to a dictionary, excluding the email and age fields
print(temp2)

temp3 = patient.model_dump_json(include=['email', "age"])# Serialize the patient data to a dictionary, excluding the email and age fields
print(temp3)

temp4 = patient.model_dump_json(exclude_unset=True)  # Serialize the patient data to a dictionary, excluding unset fields
print(temp4)