from sqlalchemy.orm import Session
from ..models.payment import User, Account, Transaction
from ..schemas.payment import UserCreate, WithdrawalRequestV1
from ..core.security import get_password_hash, verify_password
from fastapi import HTTPException, status
import uuid

def create_user(db: Session, user_in: UserCreate):
    hashed_pw = get_password_hash(user_in.password)
    db_user = User(
        username=user_in.username,
        hashed_password=hashed_pw,
        full_name=user_in.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Auto create an account for new user
    db_account = Account(
        account_number=str(uuid.uuid4().hex[:10]).upper(),
        balance=1000.0, # Starting balance for demo
        user_id=db_user.id
    )
    db.add(db_account)
    db.commit()
    
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def get_user_accounts(db: Session, user_id: int):
    return db.query(Account).filter(Account.user_id == user_id).all()

def get_account_transactions(db: Session, account_id: int):
    return db.query(Transaction).filter(Transaction.account_id == account_id).all()

def withdraw_v1(db: Session, user_id: int, request: WithdrawalRequestV1):
    account = db.query(Account).filter(
        Account.account_number == request.account_number,
        Account.user_id == user_id
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    try:
        amount_float = float(request.amount)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid amount format. Must be a numeric string.")
        
    if account.balance < amount_float:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    
    account.balance -= amount_float
    
    db_transaction = Transaction(
        account_id=account.id,
        transaction_type="withdrawal",
        amount=amount_float,
        description=request.description
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    
    return db_transaction
