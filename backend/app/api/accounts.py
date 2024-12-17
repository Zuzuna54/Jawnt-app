from fastapi import APIRouter, HTTPException, status # type: ignore
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

@router.post(
    "/internal-accounts",
    response_model=InternalAccountResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Internal Bank Account",
    description="""
    Create a new internal organization bank account.
    
    This endpoint allows creating either a funding or claims account for internal use.
    The account will be assigned a unique ID and UUID upon creation.
    """
)
async def create_internal_account(account: InternalAccountCreate):
    db_account = InternalOrganizationBankAccount(
        type=account.type,
        account_number=account.account_number,
        routing_number=account.routing_number,
        organization_id=account.organization_id
    )
    created_account = db.internal_accounts.create(db_account)
    message_queue.publish(ACCOUNT_CREATED, {"account_id": created_account.id, "type": "internal"})
    return created_account

@router.get(
    "/internal-accounts",
    response_model=List[InternalAccountResponse],
    summary="List Internal Bank Accounts",
    description="Retrieve a list of all internal organization bank accounts."
)
async def list_internal_accounts():
    return db.internal_accounts.list()

@router.patch(
    "/internal-accounts/{account_id}",
    response_model=InternalAccountResponse,
    summary="Update Internal Bank Account",
    description="""
    Update an internal organization bank account type.
    
    The account type can be changed between 'funding' and 'claims'.
    Other account details cannot be modified.
    """
)
async def update_internal_account(account_id: int, account_update: InternalAccountUpdate):
    existing_account = db.internal_accounts.get(account_id)
    if not existing_account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    existing_account.type = account_update.type
    updated_account = db.internal_accounts.update(account_id, existing_account)
    message_queue.publish(ACCOUNT_UPDATED, {"account_id": account_id, "type": "internal"})
    return updated_account

@router.delete(
    "/internal-accounts/{account_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Internal Bank Account",
    description="Delete an internal organization bank account by its ID."
)
async def delete_internal_account(account_id: int):
    # First check if account exists
    existing_account = db.internal_accounts.get(account_id)
    if not existing_account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Then attempt to delete it
    if not db.internal_accounts.delete(account_id):
        raise HTTPException(
            status_code=500,
            detail="Failed to delete account"
        )
    
    return None  # 204 No Content

@router.post(
    "/external-accounts",
    response_model=ExternalAccountResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create External Bank Account",
    description="""
    Create an external organization bank account using Plaid data.
    
    This endpoint is used after successfully completing the Plaid Link flow
    and receiving account details from Plaid.
    """
)
async def create_external_account(account: ExternalAccountCreate):
    db_account = ExternalOrganizationBankAccount(
        plaid_account_id=account.plaid_account_id,
        account_number=account.account_number,
        routing_number=account.routing_number,
        organization_id=account.organization_id,
        bank_name=account.bank_name,
        account_type=account.account_type
    )
    created_account = db.external_accounts.create(db_account)
    message_queue.publish(ACCOUNT_CREATED, {"account_id": created_account.id, "type": "external"})
    return created_account

@router.get(
    "/external-accounts",
    response_model=List[ExternalAccountResponse],
    summary="List External Bank Accounts",
    description="Retrieve a list of all external organization bank accounts."
)
async def list_external_accounts():
    return db.external_accounts.list() 