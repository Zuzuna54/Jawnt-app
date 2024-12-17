import pytest
from fastapi import status
from app.schemas.accounts import InternalAccountCreate, InternalAccountUpdate

def test_create_internal_account(client, test_db, sample_internal_account):
    """Test creating an internal account"""
    payload = {
        "type": sample_internal_account.type,
        "account_number": sample_internal_account.account_number,
        "routing_number": sample_internal_account.routing_number,
        "organization_id": sample_internal_account.organization_id
    }
    
    response = client.post("/api/v1/internal-accounts", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    
    data = response.json()
    assert data["type"] == payload["type"]
    assert data["account_number"] == payload["account_number"]
    assert data["routing_number"] == payload["routing_number"]
    assert "id" in data
    assert "uuid" in data

def test_list_internal_accounts(client, test_db, sample_internal_account):
    """Test listing internal accounts"""
    # Create an account first
    test_db.internal_accounts.create(sample_internal_account)
    
    response = client.get("/api/v1/internal-accounts")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["type"] == sample_internal_account.type

def test_update_internal_account(client, test_db, sample_internal_account):
    """Test updating an internal account"""
    # Create an account first
    created = test_db.internal_accounts.create(sample_internal_account)
    
    # Update the account type
    update_payload = {"type": "claims"}
    response = client.patch(f"/api/v1/internal-accounts/{created.id}", json=update_payload)
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["type"] == "claims"
    assert data["id"] == created.id

def test_delete_internal_account(client, test_db, sample_internal_account):
    """Test deleting an internal account"""
    # Create an account first
    created = test_db.internal_accounts.create(sample_internal_account)
    
    response = client.delete(f"/api/v1/internal-accounts/{created.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify account is deleted
    assert test_db.internal_accounts.get(created.id) is None

def test_create_external_account(client, test_db, sample_external_account):
    """Test creating an external account"""
    payload = {
        "plaid_account_id": sample_external_account.plaid_account_id,
        "account_number": sample_external_account.account_number,
        "routing_number": sample_external_account.routing_number,
        "organization_id": sample_external_account.organization_id,
        "bank_name": sample_external_account.bank_name,
        "account_type": sample_external_account.account_type
    }
    
    response = client.post("/api/v1/external-accounts", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    
    data = response.json()
    assert data["plaid_account_id"] == payload["plaid_account_id"]
    assert data["bank_name"] == payload["bank_name"]
    assert "id" in data
    assert "uuid" in data

def test_list_external_accounts(client, test_db, sample_external_account):
    """Test listing external accounts"""
    # Create an account first
    test_db.external_accounts.create(sample_external_account)
    
    response = client.get("/api/v1/external-accounts")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["plaid_account_id"] == sample_external_account.plaid_account_id
