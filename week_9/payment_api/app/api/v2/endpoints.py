from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...db.session import get_db
from ..v1.endpoints import get_current_user_id
from ...schemas.payment import (
    TransactionResponse, WithdrawalRequestV2
)
from ...services import payment_service

router = APIRouter()

@router.post("/withdraw", response_model=TransactionResponse)
def withdraw(
    request: WithdrawalRequestV2, # V2 uses float
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    return payment_service.withdraw_v2(db, user_id, request)
