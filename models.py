from pydantic import BaseModel
from typing import List, Union
from datetime import datetime, timedelta


class UserModel(BaseModel):
    username: str
    password: str

# Expense model
class ExpenseModel(BaseModel):
    description: str
    amount: float
    expensetime: Union[datetime, None]