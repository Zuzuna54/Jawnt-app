# Jawnt Backend

FastAPI backend for the Jawnt technical assessment, implementing bank account and payment management.

## Features

- In-memory database using hashmaps
- Message queue system for event handling
- RESTful API endpoints for account and payment management
- Integration with Plaid for external bank accounts
- ACH payment processing

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Endpoints

#### Accounts

- `POST /api/v1/internal-accounts` - Create internal account (SuperUser)
- `GET /api/v1/internal-accounts` - List internal accounts (SuperUser)
- `PATCH /api/v1/internal-accounts/{account_id}` - Update internal account (SuperUser)
- `DELETE /api/v1/internal-accounts/{account_id}` - Delete internal account (SuperUser)
- `POST /api/v1/external-accounts` - Create external account with Plaid (Org Admin)
- `GET /api/v1/external-accounts` - List external accounts (Org Admin)

#### Payments

- `POST /api/v1/payments/ach-debit` - Create ACH debit payment (SuperUser)
- `GET /api/v1/payments/{payment_id}/status` - Check payment status
- `GET /api/v1/payments` - List all payments (Org Admin)

#### Plaid Integration

- `POST /api/v1/plaid/create-link-token` - Create Plaid Link token
- `POST /api/v1/plaid/exchange-token` - Exchange public token and create external account

## Testing

Run tests using pytest:

```bash
pytest
```

## Architecture

- `app/models/` - Pydantic models for data structures
- `app/api/` - API routes and endpoints
- `app/services/` - Business logic and services
- `app/schemas/` - Request/Response schemas
- `lib/jawnt/` - Payment processing client code

## Plaid Integration

The application uses Plaid's Sandbox environment for testing:

- Client ID: 6758563294bbe4001b5c5279
- Secret: 386a94d4b632d57fe91b7b0f8506b3

For testing, you can use Plaid's Sandbox credentials:

- Username: user_good
- Password: pass_good
