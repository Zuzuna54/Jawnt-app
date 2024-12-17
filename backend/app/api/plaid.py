from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from app.services.plaid import plaid_service
from app.services.database import db
from app.models.base import ExternalOrganizationBankAccount

router = APIRouter()

class CreateLinkTokenResponse(BaseModel):
    link_token: str

class ExchangePublicTokenRequest(BaseModel):
    public_token: str
    organization_id: int

@router.post("/plaid/create-link-token", response_model=CreateLinkTokenResponse)
async def create_link_token(user_id: str):
    """Create a Plaid Link token for initializing Plaid Link"""
    try:
        link_token = plaid_service.create_link_token(user_id)
        return {"link_token": link_token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/plaid/exchange-token")
async def exchange_public_token(request: ExchangePublicTokenRequest):
    """Exchange public token for access token and create external account"""
    try:
        # Exchange token and get account data
        plaid_data = plaid_service.exchange_public_token(request.public_token)
        
        # Create external accounts for each Plaid account
        created_accounts = []
        for account in plaid_data['accounts']:
            if account.type in ['checking', 'savings']:
                external_account = ExternalOrganizationBankAccount(
                    plaid_account_id=account.account_id,
                    account_number=int(account.mask) if account.mask else 0,  # In real app, get from auth endpoint
                    routing_number=0,  # In real app, get from auth endpoint
                    organization_id=request.organization_id,
                    bank_name=account.name,
                    account_type=account.type
                )
                created_account = db.external_accounts.create(external_account)
                created_accounts.append(created_account)
        
        return {"message": "Accounts linked successfully", "accounts": created_accounts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 