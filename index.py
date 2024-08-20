from models import employee
from routes import employees
from fastapi import FastAPI
from config.db import engine

employee.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(employees.router, tags=['Employees'], prefix='/api/employees')

@app.get("/")
def root():
    return {"message": "Welcome to Nextrive! Powered by FastAPI"}

