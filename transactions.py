from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas, crud, database
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Transaction, TransactionType, Operator, User
from pydantic import BaseModel
from datetime import datetime
import uuid

router = APIRouter(prefix="/transactions", tags=["Transactions"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

class TransactionCreate(BaseModel):
    amount: float
    phone_number: str
    transaction_type_id: int
    operator_id: int
    user_id: int

@router.post("/")
def create_transaction(data: TransactionCreate, db: Session = Depends(get_db)):
    # Génération d'un numéro de reçu unique
    receipt_num = f"REC-{uuid.uuid4().hex[:8].upper()}"

    transaction = Transaction(
        amount=data.amount,
        phone_number=data.phone_number,
        transaction_type_id=data.transaction_type_id,
        operator_id=data.operator_id,
        user_id=data.user_id,
        receipt_number=receipt_num,
        transaction_date=datetime.utcnow().date(),
        transaction_time=datetime.utcnow().time()
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return {
        "message": "Transaction enregistrée avec succès",
        "receipt": {
            "receipt_number": transaction.receipt_number,
            "date": transaction.transaction_date,
            "time": transaction.transaction_time,
            "amount": transaction.amount,
            "phone_number": transaction.phone_number,
            "transaction_type": transaction.transaction_type.name,
            "operator": transaction.operator.name,
            "user": transaction.user.username
        }
    }

@router.get("/archive")
def get_transactions_archive(db: Session = Depends(get_db)):
    transactions = db.query(Transaction).all()
    return transactions

@router.post("/", response_model=schemas.TransactionRead)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return crud.create_transaction(db, transaction)

@router.get("/", response_model=list[schemas.TransactionRead])
def read_transactions(db: Session = Depends(get_db)):
    return crud.get_transactions(db)
