from typing import Dict, List, Literal, Optional, Union
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class BaseDBModel(BaseModel):
    id: Optional[int] = None
    uuid: UUID = Field(default_factory=uuid4)

class SuperUser(BaseDBModel):
    first_name: str
    last_name: str

class OrganizationAdministrator(BaseDBModel):
    first_name: str
    last_name: str
    organization_id: int

class InternalOrganizationBankAccount(BaseDBModel):
    type: Literal["funding", "claims"]
    account_number: int
    routing_number: int
    organization_id: int  # Foreign key to organization

class ExternalOrganizationBankAccount(BaseDBModel):
    plaid_account_id: str
    account_number: int
    routing_number: int
    organization_id: int  # Foreign key to organization
    bank_name: str
    account_type: str

class Payment(BaseDBModel):
    source_routing_number: int
    destination_routing_number: int
    amount: int  # Amount in cents
    status: Literal["PENDING", "SUCCESS", "FAILURE"] = "PENDING"
    payment_type: Literal["ACH_DEBIT", "ACH_CREDIT"]
    source_account_id: Union[str, int]  # Can be either internal or external account
    destination_account_id: Union[str, int]  # Can be either internal or external account
    idempotency_key: str