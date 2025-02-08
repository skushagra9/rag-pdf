from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import s3, search



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

app.include_router(s3.router)
app.include_router(search.router)