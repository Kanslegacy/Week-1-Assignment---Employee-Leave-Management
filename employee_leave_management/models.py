from sqlalchemy import Column, Integer, String, Date, ForeignKey
from database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String)

class Leave(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer)

    start_date = Column(Date)
    end_date = Column(Date)

    reason = Column(String)
    status = Column(String, default="Pending")