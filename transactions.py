from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas, crud, database

router = APIRouter(prefix="/transactions", tags=["Transactions"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.TransactionRead)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return crud.create_transaction(db, transaction)

@router.get("/", response_model=list[schemas.TransactionRead])
def read_transactions(db: Session = Depends(get_db)):
    return crud.get_transactions(db)
