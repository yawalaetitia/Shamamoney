from sqlalchemy.orm import Session
import models, schemas
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# USERS

def get_password_hash(password):
    return pwd_context.hash(password)

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        password=user.password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session):
    return db.query(models.User).all()

# OPERATORS
def create_operator(db: Session, operator: schemas.OperatorCreate):
    db_operator = models.Operator(name=operator.name)
    db.add(db_operator)
    db.commit()
    db.refresh(db_operator)
    return db_operator

def get_operators(db: Session):
    return db.query(models.Operator).all()

# TRANSACTION TYPES
def create_transaction_type(db: Session, transaction_type: schemas.TransactionTypeCreate):
    db_type = models.TransactionType(name=transaction_type.name)
    db.add(db_type)
    db.commit()
    db.refresh(db_type)
    return db_type

def get_transaction_types(db: Session):
    return db.query(models.TransactionType).all()

# TRANSACTIONS
def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transactions(db: Session):
    return db.query(models.Transaction).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        password=hashed_pw,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user