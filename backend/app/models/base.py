from typing import Dict, List, Literal, Optional, Union
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class SuperUser(BaseModel):
    id: int
    uid: UUID = Field(default_factory=uuid4)

class OrganizationAdministrator(BaseModel):
    id: int
    uid: UUID = Field(default_factory=uuid4)
    first_name: str
    last_name: str
    organization_id: int

class InternalOrganizationBankAccount(BaseModel):
    id: int
    uuid: UUID = Field(default_factory=uuid4)
    type: Literal["funding", "claims"]
    account_number: int
    routing_number: int
    organization_id: int  # Foreign key to organization

class ExternalOrganizationBankAccount(BaseModel):
    id: int
    uuid: UUID = Field(default_factory=uuid4)
    plaid_account_id: str
    account_number: int
    routing_number: int
    organization_id: int  # Foreign key to organization
    bank_name: str
    account_type: str

class Payment(BaseModel):
    id: int
    uuid: UUID = Field(default_factory=uuid4)
    source_routing_number: int
    destination_routing_number: int
    amount: int  # Amount in cents
    status: Literal["PENDING", "SUCCESS", "FAILURE"] = "PENDING"
    payment_type: Literal["ACH_DEBIT", "ACH_CREDIT"]
    source_account_id: Union[str, int]  # Can be either internal or external account
    destination_account_id: Union[str, int]  # Can be either internal or external account
    idempotency_key: str 