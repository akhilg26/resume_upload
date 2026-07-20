from fastapi import FastAPI, HTTPException
from app.routes import auth
from app.routes import upload

app = FastAPI()

app.include_router(auth.router)
app.include_router(upload.router)



def get_current_user():
    pass