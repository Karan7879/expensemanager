# User registration
from fastapi import APIRouter
from passlib.context import CryptContext
from db import users_collection
from datetime import datetime,timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends,HTTPException
import jwt

auth_router = APIRouter()

from models import UserModel

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "4da73e5e37d0b92abfbf31be54a38319"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@auth_router.post("/register/", response_model=UserModel)
async def register_user(user: UserModel):
    user_data = {
        "username": user.username,
        "password": password_context.hash(user.password)
    }
    user_id = users_collection.insert_one(user_data).inserted_id
    return {**user.dict(), "_id": str(user_id)}

# Token generation
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# User authentication
@auth_router.post("/token/", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_data = users_collection.find_one({"username": form_data.username})
    if not user_data or not password_context.verify(form_data.password, user_data["password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}
