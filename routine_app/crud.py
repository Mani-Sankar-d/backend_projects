from sqlalchemy.orm import Session
import models, schemas

def create_user(db:Session, user:schemas.UserCreate):
    db_user = models.User(name = user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db:Session, id:int):
    return db.query(models.User).filter(models.User.id==id).first()

def create_routine(db:Session, routine:schemas.RoutineCreate, user_id:int):
    db_routine = models.Routine(**routine.dict(), user_id=user_id)
    db.add(db_routine)
    db.commit()
    db.refresh(db_routine)
    return db_routine

def get_user_routine(db:Session, user_id:int):
    return  db.query(models.Routine).filter(models.Routine.user_id==user_id).all()

def update_routine_status(db:Session, routine_id:int, completed:bool):
    db_routine = db.query(models.Routine).filter(models.Routine.id==routine_id).first()
    if db_routine:
        db_routine.completed=completed
        db.commit()
        db.refresh(db_routine)
    return db_routine

def delete_routine(db:Session, routine_id:int):
    db_routine = db.query(models.Routine).filter(models.Routine.id==routine_id).first()
    if db_routine:
        db.delete(db_routine)
        db.commit()
        return True
    return False
