from fastapi import FastAPI
from sqlalchemy.orm import Session
from datetime import datetime

from database import engine, SessionLocal
from models import Base, Employee, Leave

print("EMPLOYEE LEAVE APP LOADED")
app = FastAPI()

Base.metadata.create_all(bind=engine)
@app.get("/")
def home():
    print("HOME ENDPOINT HIT")
    return {"message": "Leave Management API"}

# Create sample users

@app.on_event("startup")
def startup():

    db = SessionLocal()

    if db.query(Employee).count() == 0:

        employee = Employee(
            name="John",
            email="employee@gmail.com",
            password="1234",
            role="employee"
        )

        manager = Employee(
            name="Manager",
            email="manager@gmail.com",
            password="1234",
            role="manager"
        )

        db.add(employee)
        db.add(manager)
        db.commit()

    db.close()

#Employee Login APi

@app.post("/login")
def login(data: dict):

    db = SessionLocal()

    try:
        user = db.query(Employee).filter(
            Employee.email == data["email"]
        ).first()

        if not user:
            return {"message": "Invalid User"}

        if user.password != data["password"]:
            return {"message": "Wrong Password"}

        return {
            "id": user.id,
            "name": user.name,
            "role": user.role
        }

    finally:
        db.close()

#Apply Leave API

# Apply Leave API

@app.post("/apply_leave")
def apply_leave(data: dict):

    db = SessionLocal()

    try:

        leave = Leave(
            employee_id=data["employee_id"],

            start_date=datetime.strptime(
                data["start_date"],
                "%Y-%m-%d"
            ).date(),

            end_date=datetime.strptime(
                data["end_date"],
                "%Y-%m-%d"
            ).date(),

            reason=data["reason"],
            status="Pending"
        )

        db.add(leave)
        db.commit()

        return {"message": "Leave Applied"}

    finally:
        db.close()

#Leave History API

@app.get("/leave_history/{employee_id}")
def leave_history(employee_id: int):

    db = SessionLocal()

    data = db.query(Leave).filter(
        Leave.employee_id == employee_id
    ).all()

    result = []

    for leave in data:
        result.append({
            "id": leave.id,
            "employee_id": leave.employee_id,
            "start_date": str(leave.start_date),
            "end_date": str(leave.end_date),
            "reason": leave.reason,
            "status": leave.status
        })

    return result

#Manager view requests API

@app.get("/all_leaves")
def all_leaves():

    db = SessionLocal()

    leaves = db.query(Leave).all()

    result = []

    for leave in leaves:
        result.append({
            "id":leave.id,
            "employee_id":leave.employee_id,
            "reason":leave.reason,
            "status":leave.status
        })

    return result

#Apprve/Reject API

@app.put("/update_leave/{leave_id}")
def update_leave(leave_id:int,status:str):

    db = SessionLocal()

    leave = db.query(Leave).filter(
        Leave.id == leave_id
    ).first()

    leave.status = status

    db.commit()

    return {"message":"Updated"}

