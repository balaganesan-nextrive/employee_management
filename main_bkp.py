from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import mysql.connector

# Connect to the database
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="balaganesan",
    password="abc123",
    database="emp_db"
)

# Create a cursor object
cursor = mydb.cursor()

app = FastAPI()

class DBModel(BaseModel):
	firstname: str
	lastname: str
	email: str
	designation: str

#Read all employees records
@app.get("/employees", status_code=status.HTTP_302_FOUND)
def select_employees():
	select_query = "SELECT * FROM employees"
	cursor.execute(select_query)
	results = cursor.fetchall()
	return results

#Read employee record by ID
@app.get("/employees/{employee_id}", status_code=status.HTTP_200_OK)
def get_employee_by_id(employee_id: int):
    select_query = "SELECT * FROM employees WHERE id = %s"
    cursor.execute(select_query, (employee_id,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Employee not found")

#Create new employee record
@app.post("/employees", status_code=status.HTTP_201_CREATED)
def insert_user(employee: DBModel):
    insert_query = """
    INSERT INTO employees (firstname, lastname, email, designation)
    VALUES (%s, %s, %s, %s)
    """
    values = (employee.firstname, employee.lastname, employee.email, employee.designation)

    try:
        cursor.execute(insert_query, values)
        mydb.commit()
    except mysql.connector.Error as err:
        raise HTTPException(status_code=400, detail=f"Error: {err}")

    return {"message": "Employee inserted successfully"}

# Update Employee record
@app.put("/employees/{employee_id}", status_code=status.HTTP_200_OK)
def update_employee(employee_id: int, employee: DBModel):

    update_query = """
    UPDATE employees
    SET firstname = %s, lastname = %s, email = %s, designation = %s
    WHERE id = %s
    """
    values = (employee.firstname, employee.lastname, employee.email, employee.designation, employee_id)

    cursor.execute(update_query, values)
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee updated successfully"}

# Delete employee record
@app.delete("/employees/{employee_id}", status_code=status.HTTP_200_OK)
def delete_user(employee_id: int):
    delete_query = "DELETE FROM employees WHERE id = %s"
    cursor.execute(delete_query, (employee_id,))
    mydb.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}


