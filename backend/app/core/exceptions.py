from fastapi import HTTPException, status # type: ignore

class JawntException(HTTPException):
    """Base exception for Jawnt application"""
    def __init__(self, detail: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        super().__init__(status_code=status_code, detail=detail)

class AccountNotFoundException(JawntException):
    """Raised when an account is not found"""
    def __init__(self, account_id: int):
        super().__init__(
            detail=f"Account with ID {account_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

class PaymentValidationError(JawntException):
    """Raised when payment validation fails"""
    def __init__(self, detail: str):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_400_BAD_REQUEST
        )

class PlaidIntegrationError(JawntException):
    """Raised when Plaid integration fails"""
    def __init__(self, detail: str):
        super().__init__(
            detail=f"Plaid integration error: {detail}",
            status_code=status.HTTP_502_BAD_GATEWAY
        )

class UnauthorizedError(JawntException):
    """Raised when user is not authorized"""
    def __init__(self):
        super().__init__(
            detail="Not authorized to perform this action",
            status_code=status.HTTP_401_UNAUTHORIZED
        ) 