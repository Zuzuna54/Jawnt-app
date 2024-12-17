import pytest # type: ignore
from unittest.mock import patch, MagicMock # type: ignore
from fastapi import status # type: ignore

def test_create_link_token(client):
    """Test creating a Plaid link token"""
    with patch('app.services.plaid.plaid_service.create_link_token') as mock_create:
        mock_create.return_value = "test_link_token"
        
        payload = {"user_id": "test_user"}
        response = client.post("/api/v1/plaid/create-link-token", json=payload)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["link_token"] == "test_link_token"

def test_exchange_public_token(client, test_db):
    """Test exchanging a Plaid public token"""
    with patch('app.services.plaid.plaid_service.exchange_public_token') as mock_exchange:
        # Mock the Plaid service response
        mock_exchange.return_value = {
            'access_token': 'test_access_token',
            'accounts': [
                {
                    'account_id': 'test_account_id',
                    'type': 'depository',
                    'subtype': 'checking',
                    'name': 'Test Checking',
                    'account_number': '1234567890',
                    'routing_number': '987654321'
                }
            ]
        }
        
        payload = {
            "public_token": "test_public_token",
            "organization_id": 1
        }
        
        response = client.post("/api/v1/plaid/exchange-token", json=payload)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "message" in data
        assert "accounts" in data
        assert len(data["accounts"]) > 0

def test_exchange_token_with_invalid_token(client):
    """Test exchanging an invalid public token"""
    with patch('app.services.plaid.plaid_service.exchange_public_token') as mock_exchange:
        mock_exchange.side_effect = Exception("Invalid token")
        
        payload = {
            "public_token": "invalid_token",
            "organization_id": 1
        }
        
        response = client.post("/api/v1/plaid/exchange-token", json=payload)
        assert response.status_code == status.HTTP_502_BAD_GATEWAY

def test_exchange_token_with_no_eligible_accounts(client):
    """Test exchanging token with no eligible accounts"""
    with patch('app.services.plaid.plaid_service.exchange_public_token') as mock_exchange:
        # Mock response with non-checking/savings accounts
        mock_exchange.return_value = {
            'access_token': 'test_access_token',
            'accounts': [
                {
                    'account_id': 'test_account_id',
                    'type': 'credit',
                    'subtype': 'credit_card',
                    'name': 'Test Credit Card'
                }
            ]
        }
        
        payload = {
            "public_token": "test_public_token",
            "organization_id": 1
        }
        
        response = client.post("/api/v1/plaid/exchange-token", json=payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "No eligible" in response.json()["detail"]

def test_create_link_token_error_handling(client):
    """Test error handling in create link token endpoint"""
    with patch('app.services.plaid.plaid_service.create_link_token') as mock_create:
        mock_create.side_effect = Exception("Plaid API error")
        
        payload = {"user_id": "test_user"}
        response = client.post("/api/v1/plaid/create-link-token", json=payload)
        
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
