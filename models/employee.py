from sqlalchemy import Column, Integer, String, Boolean
from config.db import Base

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(50), index=True)
    lastname = Column(String(50), index=True)
    email = Column(String(50), unique=True)
    designation = Column(String(50), index=True)
