from jose import jwt
from fastapi import Request, HTTPException,Form
from datetime import datetime, timedelta
SECRET_KEY = "MY KEY"
ALGORITHM = "HS256"
ACCESS_TIME = timedelta(minutes=15)
def create_access_token(email:str):
    exp = datetime.utcnow()+ACCESS_TIME
    user_data = {'email':email,'exp':exp}
    return jwt.encode(user_data, SECRET_KEY, algorithm=ALGORITHM)

def get_token_from_cookies(request:Request):
    token = request.get("acess_token")
    if not token:
        raise HTTPException(401, detail="not authenticated")
    return token

def verify_token(token: str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        return payload
    except:
        raise HTTPException(403, detail="Invalid or expired token")
def decode(token):
    return jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)