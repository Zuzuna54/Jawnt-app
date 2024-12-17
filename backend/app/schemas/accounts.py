from typing import Literal, Optional
from pydantic import BaseModel # type: ignore
from uuid import UUID

class InternalAccountCreate(BaseModel):
    type: Literal["funding", "claims"]
    account_number: int
    routing_number: int
    organization_id: int

class InternalAccountUpdate(BaseModel):
    type: Literal["funding", "claims"]

class ExternalAccountCreate(BaseModel):
    plaid_account_id: str
    account_number: int
    routing_number: int
    organization_id: int
    bank_name: str
    account_type: str

class AccountResponse(BaseModel):
    id: int
    uuid: UUID
    account_number: int
    routing_number: int
    organization_id: int

class InternalAccountResponse(AccountResponse):
    type: Literal["funding", "claims"]

class ExternalAccountResponse(AccountResponse):
    plaid_account_id: str
    bank_name: str
    account_type: str 