# Jawnt Backend

FastAPI backend implementation for the Jawnt banking application, featuring in-memory data structures, event handling, and Plaid integration.

## Features

### Account Management

- **Internal Bank Accounts**

  - CRUD operations
  - Type validation (funding/claims)
  - Account number handling
  - Routing number validation

- **External Bank Accounts**
  - Plaid integration
  - Account validation
  - Type checking (checking/savings)
  - Real-time updates

### Payment Processing

- **ACH Debit Payments**

  - Pull funds from external accounts
  - Status tracking
  - Event publishing
  - Idempotency handling

- **ACH Credit Payments**

  - Push funds to external accounts
  - Status validation
  - Event handling
  - Error management

- **Book Payments**
  - Internal account transfers
  - Account validation
  - Status tracking
  - Event publishing

### Data Structures

- **In-Memory Database**

  - Hashmap-based storage
  - CRUD operations
  - Type-safe implementations
  - Foreign key relationships

- **Message Queue**
  - Event publishing
  - Async message handling
  - Event type system
  - Queue persistence

## Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.9+ with type hints
- **Data Storage**: In-memory hashmaps
- **Event Handling**: Custom message queue
- **API Documentation**: Swagger/OpenAPI
- **Testing**: pytest
- **Banking Integration**: Plaid API

## Project Structure

```
app/
├── api/                 # API endpoints
│   ├── accounts.py     # Account management
│   ├── payments.py     # Payment processing
│   └── plaid.py        # Plaid integration
├── core/               # Core functionality
│   ├── config.py       # Configuration
│   └── exceptions.py   # Custom exceptions
├── models/             # Data models
│   └── base.py        # Base models
├── schemas/            # Pydantic schemas
│   ├── accounts.py    # Account schemas
│   └── payments.py    # Payment schemas
├── services/          # Business logic
│   ├── database.py   # In-memory database
│   ├── queue.py      # Message queue
│   └── plaid.py      # Plaid service
└── main.py           # Application entry point
```

## Implementation Details

### Data Models

```python
class BaseDBModel(BaseModel):
    id: Optional[int] = None
    uuid: UUID = Field(default_factory=uuid4)

class InternalOrganizationBankAccount(BaseDBModel):
    type: Literal["funding", "claims"]
    account_number: int
    routing_number: int
    organization_id: int

class Payment(BaseDBModel):
    source_routing_number: int
    destination_routing_number: int
    amount: int  # Amount in cents
    status: Literal["PENDING", "SUCCESS", "FAILURE"]
    payment_type: Literal["ACH_DEBIT", "ACH_CREDIT", "BOOK"]
```

### Database Implementation

```python
class InMemoryDB(Generic[T]):
    def __init__(self):
        self._data: Dict[int, T] = {}
        self._counter = 1

    def create(self, item: T) -> T:
        item.id = self._counter
        self._data[self._counter] = item
        self._counter += 1
        return item
```

### Event System

```python
class MessageQueue:
    def __init__(self):
        self._queue = deque()
        self._handlers: Dict[str, List[Callable]] = {}

    def publish(self, event_type: str, payload: Dict[str, Any]) -> None:
        message = Message(event_type, payload)
        self._queue.append(message)
```

## Getting Started

### Prerequisites

- Python 3.9 or higher
- pip package manager
- Virtual environment tool

### Installation

1. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

```bash
cp .env.example .env
```

4. Start the development server:

```bash
uvicorn app.main:app --reload --port 8001
```

The API will be available at `http://localhost:8001`

## API Documentation

Once the server is running, access:

- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`

### Key Endpoints

#### Account Management

- `POST /api/v1/internal-accounts` - Create internal account
- `GET /api/v1/internal-accounts` - List internal accounts
- `PATCH /api/v1/internal-accounts/{id}` - Update internal account
- `DELETE /api/v1/internal-accounts/{id}` - Delete internal account
- `POST /api/v1/external-accounts` - Create external account
- `GET /api/v1/external-accounts` - List external accounts

#### Payment Processing

- `POST /api/v1/payments/ach-debit` - Create ACH debit payment
- `POST /api/v1/payments/ach-credit` - Create ACH credit payment
- `POST /api/v1/payments/book` - Create book payment
- `GET /api/v1/payments/{id}/status` - Check payment status
- `GET /api/v1/payments` - List all payments

#### Plaid Integration

- `POST /api/v1/plaid/create-link-token` - Create Plaid Link token
- `POST /api/v1/plaid/exchange-token` - Exchange public token

## Testing

Run the test suite:

```bash
pytest
```

The test suite includes:

- Unit tests for all endpoints
- Integration tests for Plaid
- Payment processing tests
- Database operation tests
- Event system tests

### Test Structure

```python
@pytest.fixture
def test_db():
    """Test database fixture"""
    test_db = Database(auto_seed=False)
    yield test_db

def test_create_payment(client, test_db):
    """Test payment creation"""
    payload = {
        "amount": 50000,
        "payment_type": "ACH_DEBIT",
        ...
    }
    response = client.post("/api/v1/payments/ach-debit", json=payload)
    assert response.status_code == 201
```

## Error Handling

- Custom exception classes
- HTTP status codes
- Detailed error messages
- Validation error handling

## Best Practices

- Type hints throughout
- SOLID principles
- Clean code architecture
- Comprehensive testing
- Detailed documentation

## Future Improvements

1. Add persistent storage
2. Implement caching
3. Add rate limiting
4. Enhance logging
5. Add metrics collection

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is part of a technical assessment and is not licensed for public use.
