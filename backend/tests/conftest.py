import pytest # type: ignore
from fastapi.testclient import TestClient # type: ignore
from app.main import app # type: ignore
from app.services.database import Database, db # type: ignore
from app.models.base import InternalOrganizationBankAccount, ExternalOrganizationBankAccount, Payment # type: ignore

@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)

@pytest.fixture
def test_db():
    """Test database fixture"""
    # Create a fresh database instance for each test with no auto-seeding
    test_db = Database(auto_seed=False)
    
    # Store the original db instance
    original_db = db
    
    # Replace the global db instance with our test instance
    import app.services.database
    app.services.database.db = test_db
    
    yield test_db
    
    # Restore the original db instance after the test
    app.services.database.db = original_db

@pytest.fixture
def sample_internal_account():
    """Sample internal account fixture"""
    return InternalOrganizationBankAccount(
        type="funding",
        account_number=123456789,
        routing_number=987654321,
        organization_id=1
    )

@pytest.fixture
def sample_external_account():
    """Sample external account fixture"""
    return ExternalOrganizationBankAccount(
        plaid_account_id="test_plaid_id",
        account_number=987654321,
        routing_number=123456789,
        organization_id=1,
        bank_name="Test Bank",
        account_type="checking"
    )

@pytest.fixture
def sample_payment():
    """Sample payment fixture"""
    return Payment(
        source_routing_number=123456789,
        destination_routing_number=987654321,
        amount=50000,  # $500.00
        payment_type="ACH_DEBIT",
        source_account_id="test_plaid_id",
        destination_account_id=1,
        idempotency_key="test_payment_1"
    )
