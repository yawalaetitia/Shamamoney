from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas, crud, database

router = APIRouter(prefix="/transaction-types", tags=["Transaction Types"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.TransactionTypeRead)
def create_type(type: schemas.TransactionTypeCreate, db: Session = Depends(get_db)):
    return crud.create_transaction_type(db, type)

@router.get("/", response_model=list[schemas.TransactionTypeRead])
def read_types(db: Session = Depends(get_db)):
    return crud.get_transaction_types(db)
