from fastapi import FastAPI, Header
from app.routes import auth
from app.routes import upload
from app.routes import create_match
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'], # front end, change when deployed
    allow_credentials=True, # able to send credentials
    allow_methods=["*"], # http methods
    allow_headers=["*"] # allows request headers
)
app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(create_match.router)




