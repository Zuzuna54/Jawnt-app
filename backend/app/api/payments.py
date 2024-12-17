from fastapi import APIRouter, HTTPException, status
from typing import List
import uuid

from app.services.database import db
from app.models.base import Payment
from app.schemas.payments import PaymentCreate, PaymentResponse
from app.services.queue import message_queue, PAYMENT_CREATED, PAYMENT_UPDATED
from lib.jawnt.client import perform_ach_debit, perform_ach_credit, get_payment_status

router = APIRouter()

@router.post(
    "/payments/ach-debit",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create ACH Debit Payment",
    description="""
    Create a new ACH debit payment to pull funds from an external account.
    
    Amount should be specified in cents (e.g., $50.00 = 5000).
    The payment will initially be in PENDING status.
    An idempotency key must be provided to prevent duplicate payments.
    """
)
async def create_ach_debit_payment(payment: PaymentCreate):
    # Call the provided client code
    response = perform_ach_debit(
        str(payment.source_account_id),
        str(payment.destination_account_id),
        payment.amount,
        payment.idempotency_key
    )
    
    # Create payment record
    db_payment = Payment(
        source_routing_number=payment.source_routing_number,
        destination_routing_number=payment.destination_routing_number,
        amount=payment.amount,
        payment_type="ACH_DEBIT",
        source_account_id=payment.source_account_id,
        destination_account_id=payment.destination_account_id,
        idempotency_key=payment.idempotency_key,
        status="PENDING"
    )
    
    created_payment = db.payments.create(db_payment)
    message_queue.publish(PAYMENT_CREATED, {
        "payment_id": created_payment.id,
        "type": "ACH_DEBIT",
        "amount": payment.amount
    })
    
    return created_payment

@router.get(
    "/payments/{payment_id}/status",
    response_model=PaymentResponse,
    summary="Check Payment Status",
    description="""
    Check the current status of a payment.
    
    This endpoint makes a long-running call to check the payment status.
    The status can be one of: PENDING, SUCCESS, or FAILURE.
    """
)
async def check_payment_status(payment_id: int):
    payment = db.payments.get(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    # Get status from client
    status = get_payment_status(str(payment.uuid))
    
    # Update payment status
    payment.status = status.value
    updated_payment = db.payments.update(payment_id, payment)
    message_queue.publish(PAYMENT_UPDATED, {
        "payment_id": payment_id,
        "status": status.value
    })
    
    return updated_payment

@router.get(
    "/payments",
    response_model=List[PaymentResponse],
    summary="List All Payments",
    description="""
    Retrieve a list of all payments.
    
    This endpoint returns all payments regardless of their status.
    Each payment includes its current status, amount, and routing information.
    """
)
async def list_payments():
    return db.payments.list() 