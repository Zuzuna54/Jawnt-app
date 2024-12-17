import pytest # type: ignore    
from unittest.mock import patch # type: ignore
from fastapi import status # type: ignore
from lib.jawnt.client import PaymentStatus, PaymentResponse # type: ignore
import uuid # type: ignore

def test_create_ach_debit_payment(client, test_db, sample_payment):
    """Test creating an ACH debit payment"""
    with patch('lib.jawnt.client.perform_ach_debit') as mock_debit:
        # Mock the external payment call
        mock_debit.return_value = PaymentResponse(
            payment_id=str(uuid.uuid4()),
            status=PaymentStatus.PENDING,
            amount=sample_payment.amount
        )
        
        payload = {
            "source_routing_number": sample_payment.source_routing_number,
            "destination_routing_number": sample_payment.destination_routing_number,
            "amount": sample_payment.amount,
            "payment_type": sample_payment.payment_type,
            "source_account_id": sample_payment.source_account_id,
            "destination_account_id": sample_payment.destination_account_id,
            "idempotency_key": sample_payment.idempotency_key
        }
        
        response = client.post("/api/v1/payments/ach-debit", json=payload)
        assert response.status_code == status.HTTP_201_CREATED
        
        data = response.json()
        assert data["amount"] == payload["amount"]
        assert data["status"] == "PENDING"
        assert data["payment_type"] == "ACH_DEBIT"
        assert "id" in data
        assert "uuid" in data

def test_check_payment_status(client, test_db, sample_payment):
    """Test checking payment status"""
    with patch('lib.jawnt.client.get_payment_status') as mock_status:
        # Create a payment first
        created = test_db.payments.create(sample_payment)
        
        # Mock the status check
        mock_status.return_value = PaymentStatus.SUCCESS
        
        response = client.get(f"/api/v1/payments/{created.id}/status")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["id"] == created.id
        assert data["status"] in ["SUCCESS", "FAILURE"]

def test_list_payments(client, test_db, sample_payment):
    """Test listing all payments"""
    # Create a payment first
    test_db.payments.create(sample_payment)
    
    response = client.get("/api/v1/payments")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["amount"] == sample_payment.amount
    assert data[0]["payment_type"] == sample_payment.payment_type

def test_payment_not_found(client, test_db):
    """Test handling non-existent payment"""
    response = client.get("/api/v1/payments/999/status")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_create_payment_with_invalid_data(client, test_db):
    """Test creating payment with invalid data"""
    invalid_payload = {
        "source_routing_number": "invalid",  # Should be int
        "destination_routing_number": 987654321,
        "amount": 50000,
        "payment_type": "ACH_DEBIT",
        "source_account_id": "test_account",
        "destination_account_id": 1,
        "idempotency_key": "test_key"
    }
    
    response = client.post("/api/v1/payments/ach-debit", json=invalid_payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
