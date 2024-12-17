from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List

from app.services.plaid import plaid_service
from app.services.database import db
from app.models.base import ExternalOrganizationBankAccount
from app.core.exceptions import PlaidIntegrationError

router = APIRouter()

class CreateLinkTokenRequest(BaseModel):
    user_id: str

class CreateLinkTokenResponse(BaseModel):
    link_token: str

class ExchangePublicTokenRequest(BaseModel):
    public_token: str
    organization_id: int

class ExchangePublicTokenResponse(BaseModel):
    message: str
    accounts: List[ExternalOrganizationBankAccount]

@router.post(
    "/plaid/create-link-token",
    response_model=CreateLinkTokenResponse,
    summary="Create Plaid Link Token",
    description="""
    Create a Link token for initializing Plaid Link in the frontend.
    
    This token is required to start the Plaid Link flow and should be used
    within 30 minutes of creation.
    """
)
async def create_link_token(request: CreateLinkTokenRequest):
    try:
        link_token = plaid_service.create_link_token(request.user_id)
        return {"link_token": link_token}
    except Exception as e:
        raise PlaidIntegrationError(str(e))

@router.post(
    "/plaid/exchange-token",
    response_model=ExchangePublicTokenResponse,
    summary="Exchange Plaid Public Token",
    description="""
    Exchange a public token received from Plaid Link for access token and account data.
    
    This endpoint should be called after successfully completing the Plaid Link flow.
    It will create ExternalOrganizationBankAccount records for each checking or savings
    account linked through Plaid.
    """
)
async def exchange_public_token(request: ExchangePublicTokenRequest):
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
        
        return {
            "message": "Accounts linked successfully",
            "accounts": created_accounts
        }
    except Exception as e:
        raise PlaidIntegrationError(str(e)) 