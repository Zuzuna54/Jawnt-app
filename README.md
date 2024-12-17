# Jawnt Technical Assessment

A full-stack banking application that demonstrates account management and payment processing capabilities using Next.js and FastAPI.

## Overview

This project implements a banking system with the following core features:

- External bank account connection via Plaid
- Internal bank account management
- ACH payment processing
- Real-time payment status tracking

## Project Structure

```
.
├── frontend/          # Next.js frontend application
│   ├── src/          # Source code
│   │   ├── app/      # Pages and layouts
│   │   ├── components/ # Reusable components
│   │   ├── hooks/    # Custom React hooks
│   │   ├── lib/      # Utility functions
│   │   └── types/    # TypeScript definitions
│   └── ...
├── backend/          # FastAPI backend application
│   ├── app/         # Application code
│   │   ├── api/     # API endpoints
│   │   ├── models/  # Data models
│   │   ├── schemas/ # Pydantic schemas
│   │   ├── services/ # Business logic
│   │   └── core/    # Core functionality
│   ├── tests/       # Test suite
│   └── lib/         # External libraries
└── docs/           # Project documentation
```

## Core Components

### Backend Architecture

1. **Data Models**

   - Base models with UUID support
   - Internal/External bank account models
   - Payment transaction models
   - Type-safe implementations

2. **Services**

   - In-memory database service
   - Message queue service
   - Plaid integration service
   - Event publishing system

3. **API Endpoints**
   - Account management
   - Payment processing
   - Plaid integration
   - Status tracking

### Frontend Architecture

1. **Pages**

   - Account management
   - Payment tracking
   - Home page

2. **Components**

   - Plaid Link integration
   - Account displays
   - Payment forms
   - Navigation

3. **Features**
   - Real-time updates
   - Error handling
   - Loading states
   - Responsive design

## Quick Start

### Prerequisites

- Node.js 18+ and pnpm for frontend
- Python 3.9+ for backend
- Git

### Frontend Setup

```bash
cd frontend
pnpm install
pnpm dev
```

The frontend will be available at `http://localhost:3000`

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

The backend API will be available at `http://localhost:8001`

## Features

### Account Management

1. **Internal Accounts**

   - Funding accounts
   - Claims accounts
   - CRUD operations
   - Type validation

2. **External Accounts**
   - Plaid integration
   - Account linking
   - Account validation
   - Real-time updates

### Payment Processing

1. **Payment Types**

   - ACH Debit (pull from external)
   - ACH Credit (push to external)
   - Book (internal transfer)

2. **Features**
   - Status tracking
   - Event publishing
   - Idempotency
   - Error handling

### Event System

1. **Message Queue**

   - Event publishing
   - Event handling
   - Status updates
   - Type safety

2. **Event Types**
   - Payment events
   - Account events
   - Status updates

## API Documentation

### Account Endpoints

```
POST /api/v1/internal-accounts  - Create internal account
GET /api/v1/internal-accounts   - List internal accounts
PATCH /api/v1/internal-accounts/{id} - Update internal account
DELETE /api/v1/internal-accounts/{id} - Delete internal account
POST /api/v1/external-accounts  - Create external account
GET /api/v1/external-accounts   - List external accounts
```

### Payment Endpoints

```
POST /api/v1/payments/ach-debit - Create ACH debit payment
POST /api/v1/payments/ach-credit - Create ACH credit payment
POST /api/v1/payments/book     - Create book payment
GET /api/v1/payments/{id}/status - Check payment status
GET /api/v1/payments          - List all payments
```

### Plaid Endpoints

```
POST /api/v1/plaid/create-link-token - Create Plaid Link token
POST /api/v1/plaid/exchange-token    - Exchange public token
```

## Testing

The project includes comprehensive test coverage:

```bash
# Run backend tests
cd backend
pytest

# Run frontend tests (when implemented)
cd frontend
pnpm test
```

## Tech Stack

### Frontend

- Next.js 14 with App Router
- TypeScript
- Tailwind CSS
- Plaid Link SDK
- Axios for API calls

### Backend

- FastAPI
- Python with type hints
- In-memory database
- Message queue system
- Plaid API integration

## Documentation

- [Frontend Documentation](./frontend/README.md)
- [Backend Documentation](./backend/README.md)
- [Implementation Status](./REQUIREMENTS.md)
- [Development Tickets](./TICKETS.md)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is part of a technical assessment and is not licensed for public use.
