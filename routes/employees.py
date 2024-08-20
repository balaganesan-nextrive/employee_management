from schemas.employee import EmployeeBaseSchema
from models.employee import Employee
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from config.db import get_db

router = APIRouter()

@router.get('/')
def get_employees(db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    return {'status': 'success', 'results': len(employees), 'employees': employees}


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_employee(payload: EmployeeBaseSchema, db: Session = Depends(get_db)):
    new_employee = Employee(**payload.dict())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return {"status": "success", "employee": new_employee}


@router.put('/{id}')
def update_employee(id: int, payload: EmployeeBaseSchema, db: Session = Depends(get_db)):
    employee_query = db.query(Employee).filter(Employee.id == id)
    db_employee = employee_query.first()

    if not db_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No employee with this ID: {id} found')
    update_data = payload.dict()
    employee_query.filter(Employee.id == id).update(update_data,
                                                       synchronize_session=False)
    db.commit()
    db.refresh(db_employee)
    return {"status": "success", "employee": db_employee}

@router.get('/{id}')
def get_employee(id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No employee with this ID: {id} found")
    return {"status": "success", "employee": employee}

@router.delete('/{id}')
def delete_post(id: int, db: Session = Depends(get_db)):
    employee_query = db.query(Employee).filter(Employee.id == id)
    employee = employee_query.first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No employee with this ID: {id} found')
    employee_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch('/{id}')
def update_employee(id: int, payload: EmployeeBaseSchema, db: Session = Depends(get_db)):
    employee_query = db.query(Employee).filter(Employee.id == id)
    db_employee = employee_query.first()

    if not db_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No employee with this ID: {id} found')
    update_data = payload.dict(exclude_unset=True)

    employee_query.filter(Employee.id == id).update(update_data,
                                                       synchronize_session=False)
    db.commit()
    db.refresh(db_employee)
    return {"status": "success", "employee": db_employee}