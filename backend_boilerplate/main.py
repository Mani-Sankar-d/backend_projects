from fastapi import FastAPI,Request,HTTPException
import asyncio
from routes import auth
from database.sql import engine
from models.user import Base
import time
app = FastAPI()
Base.metadata.create_all(engine)
app.include_router(auth.router)

