from typing import Dict, Any
import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
import time

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
            
            exchange_response = self.client.item_public_token_exchange(exchange_request)
            access_token = exchange_response['access_token']
            
            # Store access token in memory (in production this should be encrypted and stored in a secure database)
            if not hasattr(self, 'access_tokens'):
                self.access_tokens = {}
            self.access_tokens[access_token] = {
                'created_at': time.time(),
                'item_id': exchange_response['item_id']
            }
            
            # Get account details
            accounts_response = self.client.accounts_get({
                'access_token': access_token
            })
            
            # Get auth details for account and routing numbers
            auth_response = self.client.auth_get({
                'access_token': access_token
            })
            
            # Combine account and auth data
            accounts = accounts_response['accounts']
            for account in accounts:
                for auth_account in auth_response['numbers']['ach']:
                    if account['account_id'] == auth_account['account_id']:
                        account['account_number'] = auth_account['account']
                        account['routing_number'] = auth_account['routing']
                        break
            
            return {
                'access_token': access_token,
                'accounts': accounts
            }
        except Exception as e:
            raise PlaidIntegrationError(f"Failed to exchange public token: {str(e)}")

# Global Plaid service instance
plaid_service = PlaidService() 