from typing import Optional
from pydantic import BaseModel

class EmployeeBaseSchema(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    designation: Optional[str] = None
