from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sheets_router import sheets_router

load_dotenv()
app = FastAPI()

origins = ["http://localhost:8000"]  # TODO

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sheets_router)
