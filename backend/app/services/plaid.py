from typing import Dict, Any
import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest

from app.core.config import settings
from app.core.exceptions import PlaidIntegrationError

class PlaidService:
    def __init__(self):
        try:
            configuration = plaid.Configuration(
                host=plaid.Environment.Sandbox if settings.PLAID_ENV == "sandbox" else plaid.Environment.Development,
                api_key={
                    'clientId': settings.PLAID_CLIENT_ID,
                    'secret': settings.PLAID_SECRET,
                }
            )
            
            api_client = plaid.ApiClient(configuration)
            self.client = plaid_api.PlaidApi(api_client)
        except Exception as e:
            raise PlaidIntegrationError(f"Failed to initialize Plaid client: {str(e)}")
    
    def create_link_token(self, user_id: str) -> str:
        """Create a Link token for initializing Plaid Link"""
        try:
            request = LinkTokenCreateRequest(
                products=[Products("auth")],
                client_name="Jawnt App",
                country_codes=[CountryCode("US")],
                language="en",
                user=LinkTokenCreateRequestUser(
                    client_user_id=user_id
                )
            )
            
            response = self.client.link_token_create(request)
            return response['link_token']
        except Exception as e:
            raise PlaidIntegrationError(f"Failed to create link token: {str(e)}")
    
    def exchange_public_token(self, public_token: str) -> Dict[str, Any]:
        """Exchange public token for access token and account data"""
        try:
            exchange_request = ItemPublicTokenExchangeRequest(
                public_token=public_token
            )
            
            response = self.client.item_public_token_exchange(exchange_request)
            access_token = response['access_token']
            
            # Get account details
            account_response = self.client.accounts_get(access_token)
            return {
                'access_token': access_token,
                'accounts': account_response['accounts']
            }
        except Exception as e:
            raise PlaidIntegrationError(f"Failed to exchange public token: {str(e)}")

# Global Plaid service instance
plaid_service = PlaidService() 