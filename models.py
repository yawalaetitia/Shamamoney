from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from database import Base

class UserRole(enum.Enum):
    admin = "admin"
    super_admin = "super_admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.admin)

class Operator(Base):
    __tablename__ = "operators"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class TransactionType(Base):
    __tablename__ = "transaction_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    transaction_type_id = Column(Integer, ForeignKey("transaction_types.id"))
    operator_id = Column(Integer, ForeignKey("operators.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    transaction_type = relationship("TransactionType")
    operator = relationship("Operator")
    user = relationship("User")
