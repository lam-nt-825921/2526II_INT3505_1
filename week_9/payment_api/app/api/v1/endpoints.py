from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from ...db.session import get_db
from ...schemas.payment import (
    UserCreate, UserResponse, Token, LoginRequest, 
    AccountResponse, TransactionResponse, WithdrawalRequestV1
)
from ...services import payment_service
from ...core.security import create_access_token, SECRET_KEY, ALGORITHM
from typing import List

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/login")

async def get_current_user_id(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return int(user_id)
    except (JWTError, ValueError):
        raise credentials_exception

@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    return payment_service.create_user(db, user_in)

@router.post("/login", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = payment_service.authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/accounts", response_model=List[AccountResponse])
def get_accounts(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return payment_service.get_user_accounts(db, user_id)

@router.get("/accounts/{account_id}/transactions", response_model=List[TransactionResponse])
def get_transactions(
    account_id: int, 
    user_id: int = Depends(get_current_user_id), 
    db: Session = Depends(get_db)
):
    # For simplicity, we assume account belongs to user in service or here
    return payment_service.get_account_transactions(db, account_id)

@router.post("/withdraw", response_model=TransactionResponse)
def withdraw(
    request: WithdrawalRequestV1,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    # X-API-Version header can be checked here or globally
    return payment_service.withdraw_v1(db, user_id, request)
