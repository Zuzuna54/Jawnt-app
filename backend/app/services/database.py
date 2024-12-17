from typing import Dict, List, Optional, TypeVar, Generic, Type
from pydantic import BaseModel # type: ignore
from app.models.base import (
    SuperUser,
    OrganizationAdministrator,
    InternalOrganizationBankAccount,
    ExternalOrganizationBankAccount,
    Payment
)

T = TypeVar('T', bound=BaseModel)

class InMemoryDB(Generic[T]):
    def __init__(self):
        self._data: Dict[int, T] = {}
        self._counter = 1

    def create(self, item: T) -> T:
        item.id = self._counter
        self._data[self._counter] = item
        self._counter += 1
        return item

    def get(self, id: int) -> Optional[T]:
        return self._data.get(id)

    def list(self) -> List[T]:
        return list(self._data.values())

    def update(self, id: int, item: T) -> Optional[T]:
        if id in self._data:
            item.id = id  # Ensure ID is preserved
            self._data[id] = item
            return item
        return None

    def delete(self, id: int) -> bool:
        """Delete an item from the database by ID"""
        try:
            del self._data[id]
            return True
        except KeyError:
            return False

    def clear(self) -> None:
        """Clear all data from the database"""
        self._data.clear()
        self._counter = 1

class Database:
    def __init__(self, auto_seed: bool = True):
        # Initialize all collections
        self.super_users = InMemoryDB[SuperUser]()
        self.org_admins = InMemoryDB[OrganizationAdministrator]()
        self.internal_accounts = InMemoryDB[InternalOrganizationBankAccount]()
        self.external_accounts = InMemoryDB[ExternalOrganizationBankAccount]()
        self.payments = InMemoryDB[Payment]()
        
        # Add seed data if auto_seed is True
        if auto_seed:
            self._seed_data()

    def _seed_data(self):
        """Seed the database with initial data"""
        # Only seed if collections are empty
        if not self.internal_accounts.list():
            funding_account = InternalOrganizationBankAccount(
                type="funding",
                account_number=123456789,
                routing_number=987654321,
                organization_id=1
            )
            claims_account = InternalOrganizationBankAccount(
                type="claims",
                account_number=987654321,
                routing_number=123456789,
                organization_id=1
            )
            self.internal_accounts.create(funding_account)
            self.internal_accounts.create(claims_account)

        if not self.external_accounts.list():
            chase_account = ExternalOrganizationBankAccount(
                plaid_account_id="chase_checking_1",
                account_number=111222333,
                routing_number=444555666,
                organization_id=1,
                bank_name="Chase Bank",
                account_type="checking"
            )
            wells_fargo_account = ExternalOrganizationBankAccount(
                plaid_account_id="wells_savings_1",
                account_number=777888999,
                routing_number=111222333,
                organization_id=1,
                bank_name="Wells Fargo",
                account_type="savings"
            )
            self.external_accounts.create(chase_account)
            self.external_accounts.create(wells_fargo_account)

        if not self.super_users.list():
            super_user = SuperUser(
                first_name="Admin",
                last_name="User"
            )
            self.super_users.create(super_user)

        if not self.org_admins.list():
            org_admin = OrganizationAdministrator(
                first_name="Org",
                last_name="Admin",
                organization_id=1
            )
            self.org_admins.create(org_admin)

        if not self.payments.list():
            payment1 = Payment(
                source_routing_number=444555666,
                destination_routing_number=987654321,
                amount=50000,  # $500.00
                status="SUCCESS",
                payment_type="ACH_DEBIT",
                source_account_id="chase_checking_1",
                destination_account_id=1,  # funding account
                idempotency_key="seed_payment_1"
            )
            payment2 = Payment(
                source_routing_number=111222333,
                destination_routing_number=123456789,
                amount=75000,  # $750.00
                status="PENDING",
                payment_type="ACH_DEBIT",
                source_account_id="wells_savings_1",
                destination_account_id=2,  # claims account
                idempotency_key="seed_payment_2"
            )
            self.payments.create(payment1)
            self.payments.create(payment2)

# Global database instance
db = Database() 