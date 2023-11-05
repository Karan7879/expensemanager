from datetime import datetime
import jwt
from models import ExpenseModel
from models import UserModel
from db import users_collection,expenses_collection
from fastapi import Depends, HTTPException
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


expenses = APIRouter()

current_datetime = datetime.now()

SECRET_KEY = "4da73e5e37d0b92abfbf31be54a38319"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@expenses.post("/expenses/", response_model=ExpenseModel)
async def create_expense(expense: ExpenseModel, current_user: str = Depends(oauth2_scheme)):
    decoded_token = jwt.decode(current_user, SECRET_KEY, algorithms=[ALGORITHM])
    username = decoded_token.get("sub")
    user_data = users_collection.find_one({"username": username})
    if not user_data:
        raise HTTPException(status_code=400, detail="User not found")
    expense_data = {
        "user_id": user_data["_id"],
        "description": expense.description,
        "amount": expense.amount,
        "expensetime":current_datetime
    }
    expense_id = expenses_collection.insert_one(expense_data).inserted_id
    return {**expense.dict(), "_id": str(expense_id)}
from typing import List
# Get expenses for the authenticated user
@expenses.get("/expenses/", response_model=List[ExpenseModel])
async def get_expenses(current_user: str = Depends(oauth2_scheme)):
    # print(current_user.)
    decoded_token = jwt.decode(current_user, SECRET_KEY, algorithms=[ALGORITHM])
    username = decoded_token.get("sub")
    user_data = users_collection.find_one({"username": username})
    if not user_data:
        raise HTTPException(status_code=400, detail="User not found")
    user_id = user_data["_id"]
    user_expenses = []
    for expense in expenses_collection.find({"user_id": user_id}):
        user_expenses.append(ExpenseModel(**expense))
    return user_expenses
