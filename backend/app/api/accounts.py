from fastapi import APIRouter, HTTPException, status
from typing import List

from app.services.database import db
from app.models.base import InternalOrganizationBankAccount, ExternalOrganizationBankAccount
from app.schemas.accounts import (
    InternalAccountCreate,
    InternalAccountUpdate,
    ExternalAccountCreate,
    InternalAccountResponse,
    ExternalAccountResponse,
)
from app.services.queue import message_queue, ACCOUNT_CREATED, ACCOUNT_UPDATED

router = APIRouter()

# Internal Account Endpoints (SuperUser only)
@router.post("/internal-accounts", response_model=InternalAccountResponse, status_code=status.HTTP_201_CREATED)
async def create_internal_account(account: InternalAccountCreate):
    """Create an internal organization bank account (SuperUser only)"""
    db_account = InternalOrganizationBankAccount(**account.dict())
    created_account = db.internal_accounts.create(db_account)
    
    # Publish event to message queue
    message_queue.publish(ACCOUNT_CREATED, {"account_id": created_account.id, "type": "internal"})
    
    return created_account

@router.get("/internal-accounts", response_model=List[InternalAccountResponse])
async def list_internal_accounts():
    """List all internal organization bank accounts (SuperUser only)"""
    return db.internal_accounts.list()

@router.patch("/internal-accounts/{account_id}", response_model=InternalAccountResponse)
async def update_internal_account(account_id: int, account_update: InternalAccountUpdate):
    """Update an internal organization bank account type (SuperUser only)"""
    existing_account = db.internal_accounts.get(account_id)
    if not existing_account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    existing_account.type = account_update.type
    updated_account = db.internal_accounts.update(account_id, existing_account)
    
    # Publish event to message queue
    message_queue.publish(ACCOUNT_UPDATED, {"account_id": account_id, "type": "internal"})
    
    return updated_account

@router.delete("/internal-accounts/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_internal_account(account_id: int):
    """Delete an internal organization bank account (SuperUser only)"""
    if not db.internal_accounts.delete(account_id):
        raise HTTPException(status_code=404, detail="Account not found")

# External Account Endpoints (Organization Administrator)
@router.post("/external-accounts", response_model=ExternalAccountResponse, status_code=status.HTTP_201_CREATED)
async def create_external_account(account: ExternalAccountCreate):
    """Create an external organization bank account using Plaid (Organization Administrator only)"""
    db_account = ExternalOrganizationBankAccount(**account.dict())
    created_account = db.external_accounts.create(db_account)
    
    # Publish event to message queue
    message_queue.publish(ACCOUNT_CREATED, {"account_id": created_account.id, "type": "external"})
    
    return created_account

@router.get("/external-accounts", response_model=List[ExternalAccountResponse])
async def list_external_accounts():
    """List all external organization bank accounts (Organization Administrator only)"""
    return db.external_accounts.list() 