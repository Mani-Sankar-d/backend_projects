from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models, schemas, crud
from database import SessionLocal, engine, Base


Base.metadata.create_all(bind=engine)

app=FastAPI()
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/users/', response_model=schemas.User)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get('/users/{user_id}/routines', response_model=List[schemas.Routine])
def read_user_routines(user_id:int, db:Session=Depends(get_db)):
    return crud.get_user_routine(db, user_id)

@app.post('/users/{user_id}/routines/', response_model=schemas.Routine)
def create_user_routine(user_id:int, routine:schemas.RoutineCreate, db:Session=Depends(get_db)):
    return crud.create_routine(db, routine, user_id)
@app.post('/routines/{routine_id}', response_model=schemas.Routine)
def update_routine_status(routine_id:int,completed:bool ,db:Session=Depends(get_db)):
    return crud.update_routine_status(db, routine_id,completed)

@app.delete('/delete/{routine_id}', response_model=schemas.Routine)
def delete_routine(routine_id:int, db:Session=Depends(get_db)):
    deleted = crud.delete_routine(db, routine_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Routine not found")
    return {'detail': 'routine deleted'}