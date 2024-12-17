from typing import Dict, Any
import plaid # type: ignore
from plaid.api import plaid_api # type: ignore  
from plaid.model.link_token_create_request import LinkTokenCreateRequest # type: ignore
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser # type: ignore
from plaid.model.products import Products # type: ignore
from plaid.model.country_code import CountryCode # type: ignore
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest # type: ignore
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
            print(f"Starting token exchange process with token: {public_token[:10]}...")
            if not public_token:
                raise PlaidIntegrationError("Public token is required")

            try:
                print("Creating exchange request...")
                exchange_request = ItemPublicTokenExchangeRequest(
                    public_token=public_token
                )
                
                print("Calling Plaid API to exchange token...")
                exchange_response = self.client.item_public_token_exchange(exchange_request)
                access_token = exchange_response['access_token']
                print(f"Successfully exchanged for access token: {access_token[:10]}...")
            except plaid.ApiException as e:
                print(f"Plaid API error during token exchange: {str(e)}")
                print(f"Error code: {getattr(e, 'code', 'unknown')}")
                print(f"Error type: {getattr(e, 'type', 'unknown')}")
                raise PlaidIntegrationError(f"Failed to exchange token: {str(e)}")
            except KeyError as e:
                print(f"Unexpected response format: {exchange_response}")
                raise PlaidIntegrationError(f"Invalid response format: missing {str(e)}")
            
            # Store access token in memory
            if not hasattr(self, 'access_tokens'):
                self.access_tokens = {}
            self.access_tokens[access_token] = {
                'created_at': time.time(),
                'item_id': exchange_response['item_id']
            }
            print("Access token stored in memory")
            
            try:
                print("Fetching account details...")
                accounts_response = self.client.accounts_get({
                    'access_token': access_token
                })
                print(f"Retrieved {len(accounts_response['accounts'])} accounts")
                
                print("Fetching auth details...")
                auth_response = self.client.auth_get({
                    'access_token': access_token
                })
                print(f"Retrieved auth details for {len(auth_response['numbers']['ach'])} accounts")
            except plaid.ApiException as e:
                print(f"Plaid API error during data fetch: {str(e)}")
                print(f"Error code: {getattr(e, 'code', 'unknown')}")
                print(f"Error type: {getattr(e, 'type', 'unknown')}")
                raise PlaidIntegrationError(f"Failed to fetch account details: {str(e)}")
            except KeyError as e:
                print(f"Unexpected response format in accounts/auth: {str(e)}")
                if 'accounts_response' in locals():
                    print(f"Accounts response: {accounts_response}")
                if 'auth_response' in locals():
                    print(f"Auth response: {auth_response}")
                raise PlaidIntegrationError(f"Invalid response format: missing {str(e)}")
            
            # Combine account and auth data
            accounts = accounts_response['accounts']
            for account in accounts:
                account_id = account['account_id']
                print(f"Processing account {account_id}")
                account_type = account.get('type', 'unknown')
                account_subtype = account.get('subtype', 'unknown')
                print(f"Account type: {account_type}, subtype: {account_subtype}")
                print(f"Raw account data: {account}")
                
                # Find matching auth details
                auth_numbers = auth_response.get('numbers', {}).get('ach', [])
                print(f"Available auth details: {auth_numbers}")
                
                for auth_account in auth_numbers:
                    if account_id == auth_account['account_id']:
                        account['account_number'] = auth_account['account']
                        account['routing_number'] = auth_account['routing']
                        print(f"Added auth details to account {account_id}")
                        break
                else:
                    print(f"No auth details found for account {account_id}")
                    # Set default values if no auth details found
                    account['account_number'] = '0000'
                    account['routing_number'] = '0000'
            
            return {
                'access_token': access_token,
                'accounts': accounts
            }
        except PlaidIntegrationError:
            raise
        except Exception as e:
            print(f"Unexpected error in exchange_public_token: {str(e)}")
            print(f"Error type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            raise PlaidIntegrationError(f"Unexpected error: {str(e)}")

# Global Plaid service instance
plaid_service = PlaidService() 