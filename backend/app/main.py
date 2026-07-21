from fastapi import FastAPI, HTTPException, Header
from app.routes import auth
from app.routes import upload
from app.routes import create_match
from dotenv import load_dotenv
import os

app = FastAPI()

app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(create_match.router)




