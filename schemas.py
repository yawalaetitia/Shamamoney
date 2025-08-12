from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime

class UserRole(str, Enum):
    admin = "admin"
    super_admin = "super_admin"

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    role: UserRole

class UserRead(UserBase):
    id: int
    role: UserRole
    class Config:
        orm_mode = True

class OperatorBase(BaseModel):
    name: str

class OperatorCreate(OperatorBase): pass

class OperatorRead(OperatorBase):
    id: int
    class Config:
        orm_mode = True

class TransactionTypeBase(BaseModel):
    name: str

class TransactionTypeCreate(TransactionTypeBase): pass

class TransactionTypeRead(TransactionTypeBase):
    id: int
    class Config:
        from_attributes = True

class TransactionBase(BaseModel):
    amount: float
    transaction_type_id: int
    operator_id: int
    operator_name:str
    user_id: int

class TransactionCreate(TransactionBase): pass

class TransactionRead(TransactionBase):
    id: int
    timestamp: datetime
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserLogin(BaseModel):
    username: str
    password: str
