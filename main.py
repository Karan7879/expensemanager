# main.py
from fastapi import FastAPI, Depends, HTTPException
from expenses_manage import expenses
from users import auth_router


app = FastAPI()
app.include_router(auth_router)
app.include_router(expenses)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
