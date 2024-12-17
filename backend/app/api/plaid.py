from fastapi import APIRouter, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore
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
        print(f"Received exchange token request for organization {request.organization_id}")
        
        # Exchange token and get account data
        plaid_data = plaid_service.exchange_public_token(request.public_token)
        print(f"Successfully retrieved Plaid data with {len(plaid_data['accounts'])} accounts")
        
        # Create external accounts for each Plaid account
        created_accounts = []
        for account in plaid_data['accounts']:
            account_id = account.get('account_id')
            account_type = str(account.get('type', '')).lower().strip()
            account_subtype = str(account.get('subtype', '')).lower().strip()
            
            print(f"\nProcessing Plaid account: {account_id}")
            print(f"Account type: {account_type}, subtype: {account_subtype}")
            print(f"Checking eligibility:")
            print(f"- Is depository? {account_type == 'depository'}")
            print(f"- Has valid subtype? {account_subtype in ['checking', 'savings']}")
            
            # Check if account is depository type with checking/savings subtype
            is_eligible = (account_type == 'depository' and account_subtype in ['checking', 'savings'])
            if is_eligible:
                try:
                    print(f"✓ Account is eligible: {account_subtype} account")
                    
                    # Get account and routing numbers from the account data
                    account_number = str(account.get('account_number', '0'))
                    routing_number = str(account.get('routing_number', '0'))
                    print(f"Account details found:")
                    print(f"- Account number: {account_number[:4] if len(account_number) >= 4 else account_number}...")
                    print(f"- Routing number: {routing_number}")
                    
                    # Convert string numbers to integers, handling any non-numeric characters
                    try:
                        account_number = int(''.join(filter(str.isdigit, account_number)))
                        routing_number = int(''.join(filter(str.isdigit, routing_number)))
                        print(f"✓ Successfully converted account and routing numbers to integers")
                    except ValueError as e:
                        print(f"✗ Error converting account/routing numbers: {str(e)}")
                        account_number = 0
                        routing_number = 0
                    
                    external_account = ExternalOrganizationBankAccount(
                        plaid_account_id=account_id,
                        account_number=account_number,
                        routing_number=routing_number,
                        organization_id=request.organization_id,
                        bank_name=account.get('name', 'Unknown Bank'),
                        account_type=account_subtype
                    )
                    print(f"✓ Created ExternalOrganizationBankAccount object")
                    
                    created_account = db.external_accounts.create(external_account)
                    if created_account:
                        print(f"✓ Successfully saved {account_subtype} account to database: {created_account.id}")
                        created_accounts.append(created_account)
                    else:
                        print(f"✗ Failed to create account in database: {account_id}")
                        raise HTTPException(
                            status_code=500,
                            detail=f"Failed to create external account for {account_id}"
                        )
                except ValueError as e:
                    print(f"✗ Value error processing account: {str(e)}")
                    print(f"Account data that caused error: {account}")
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid account data: {str(e)}"
                    )
                except Exception as e:
                    print(f"✗ Error creating external account: {str(e)}")
                    print(f"Error type: {type(e)}")
                    import traceback
                    print(f"Traceback: {traceback.format_exc()}")
                    raise HTTPException(
                        status_code=500,
                        detail=f"Error creating external account: {str(e)}"
                    )
            else:
                print(f"✗ Account is not eligible - type: {account_type}, subtype: {account_subtype}")
        
        if not created_accounts:
            print("\nNo eligible accounts found in Plaid response")
            print(f"Account types received: {[(acc.get('type'), acc.get('subtype')) for acc in plaid_data['accounts']]}")
            raise HTTPException(
                status_code=400,
                detail="No eligible checking or savings accounts found"
            )
        
        print(f"\n✓ Successfully created {len(created_accounts)} external accounts")
        return {
            "message": f"Successfully linked {len(created_accounts)} accounts",
            "accounts": created_accounts
        }
    except PlaidIntegrationError as e:
        print(f"✗ Plaid integration error: {str(e)}")
        raise HTTPException(status_code=502, detail=str(e))
    except ValueError as e:
        print(f"✗ Value error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e)) 