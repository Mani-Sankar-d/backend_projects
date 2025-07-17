from fastapi import APIRouter, Form, Depends, Response, Request,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User
from database.sql import SessionLocal,sessionmaker
from passlib.context import CryptContext
from utils.jwt import create_access_token, decode
import time
import asyncio
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
SECRET_KEY = "MY KEY"
ALGORITHM = "HS256"
async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/register")
async def register(email: str = Form(...), password: str = Form(...), db = Depends(get_db)):
    hashed_pw = pwd_context.hash(password)
    user = User(email=email,hashed_password=hashed_pw)
    print(f"creation of user {email} initiated")
    db.add(user)
    await db.commit()
    return {'msg':'user created successfully'}
@router.post("/login")
async def login(response: Response, db=Depends(get_db) ,email:str = Form(...), password:str=Form(...)):
    response.delete_cookie("access_token")
    result = await db.execute(select(User).where(User.email==email))
    user = result.scalars().first()
    if not user: 
        return {'msg':'first register bro'}
    is_true = pwd_context.verify(password, user.hashed_password)
    if(is_true==False):
        return {'msg':'dont try to fraud'}
    token = create_access_token(email=email)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        path="/",
        secure=False 
    )
    return {'msg':'login successsful cookie set'}
@router.post('/logout')
async def logout(response:Response, request:Request):
    if(request.cookies.get("access_token") == None): return {'msg':'login first bro'}
    response.delete_cookie("access_token")
    return {'msg':'logout successful'}
@router.get('/data')
async def get(request:Request, db=Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return {'msg':'first register urself'}
    try:
        data = decode(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    result = await db.execute(select(User).where(User.email==data['email']))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {'data': user.data}