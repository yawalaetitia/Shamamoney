from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from _utils import get_current_user
from fastapi import Depends
import schemas, crud, models, database

router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    return crud.create_user(db, user)

@router.get("/", response_model=list[schemas.UserRead])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@router.get("/secure", dependencies=[Depends(get_current_user)])
def secure_zone():
    return {"message": "Tu es connecté"}