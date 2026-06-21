from pydantic import BaseModel
from datetime import date

class LoginSchema(BaseModel):
    email: str
    password: str

class LeaveSchema(BaseModel):
    employee_id: int
    start_date: date
    end_date: date
    reason: str