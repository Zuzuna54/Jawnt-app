from typing import Literal, Union
from pydantic import BaseModel # type: ignore
from uuid import UUID

class PaymentCreate(BaseModel):
    source_routing_number: int
    destination_routing_number: int
    amount: int
    payment_type: Literal["ACH_DEBIT", "ACH_CREDIT", "BOOK"]
    source_account_id: Union[str, int]
    destination_account_id: Union[str, int]
    idempotency_key: str

class PaymentResponse(BaseModel):
    id: int
    uuid: UUID
    source_routing_number: int
    destination_routing_number: int
    amount: int
    status: Literal["PENDING", "SUCCESS", "FAILURE"]
    payment_type: Literal["ACH_DEBIT", "ACH_CREDIT", "BOOK"]
    source_account_id: Union[str, int]
    destination_account_id: Union[str, int]
    idempotency_key: str 