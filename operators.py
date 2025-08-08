from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas, crud, database

router = APIRouter(prefix="/operators", tags=["Operators"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.OperatorRead)
def create_operator(operator: schemas.OperatorCreate, db: Session = Depends(get_db)):
    return crud.create_operator(db, operator)

@router.get("/", response_model=list[schemas.OperatorRead])
def read_operators(db: Session = Depends(get_db)):
    return crud.get_operators(db)
