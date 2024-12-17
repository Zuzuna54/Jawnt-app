from typing import Dict, Any
import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest

class PlaidService:
    def __init__(self):
        configuration = plaid.Configuration(
            host=plaid.Environment.Sandbox,
            api_key={
                'clientId': '6758563294bbe4001b5c5279',
                'secret': '386a94d4b632d57fe91b7b0f8506b3',
            }
        )
        
        api_client = plaid.ApiClient(configuration)
        self.client = plaid_api.PlaidApi(api_client)
    
    def create_link_token(self, user_id: str) -> str:
        """Create a Link token for initializing Plaid Link"""
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
    
    def exchange_public_token(self, public_token: str) -> Dict[str, Any]:
        """Exchange public token for access token and account data"""
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

# Global Plaid service instance
plaid_service = PlaidService() 