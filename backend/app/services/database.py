from typing import Dict, List, Optional, TypeVar, Generic, Type
from pydantic import BaseModel

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
            self._data[id] = item
            return item
        return None

    def delete(self, id: int) -> bool:
        if id in self._data:
            del self._data[id]
            return True
        return False

class Database:
    def __init__(self):
        from app.models.base import (
            SuperUser,
            OrganizationAdministrator,
            InternalOrganizationBankAccount,
            ExternalOrganizationBankAccount,
            Payment
        )
        
        self.super_users = InMemoryDB[SuperUser]()
        self.org_admins = InMemoryDB[OrganizationAdministrator]()
        self.internal_accounts = InMemoryDB[InternalOrganizationBankAccount]()
        self.external_accounts = InMemoryDB[ExternalOrganizationBankAccount]()
        self.payments = InMemoryDB[Payment]()

# Global database instance
db = Database() 