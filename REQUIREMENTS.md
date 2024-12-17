# Technical Assessment Requirements

## Core Concepts to Demonstrate

- [ ] Next.js fundamentals (components, pages, etc)
- [ ] Styling fundamentals (flex, flexbox, etc)
- [x] Data fundamentals (databases, queues)
  - Implemented in-memory database with hashmaps
  - Implemented message queue system
- [x] REST fundamentals (GET, POST, PATCH, PUT)
  - Implemented all required REST endpoints
- [x] Domain logic fundamentals
  - Implemented core banking domain models
  - Proper separation of concerns
- [ ] Testing fundamentals

## Backend Requirements (✓ Completed)

### Setup and Structure

- [x] FastAPI project setup
- [x] Python type hints throughout the codebase
- [x] In-memory database using hashmaps
- [x] Message queue system
- [x] Project structure with proper separation of concerns

### Models

- [x] SuperUser model
- [x] OrganizationAdministrator model
- [x] InternalOrganizationBankAccount model
- [x] ExternalOrganizationBankAccount model
- [x] Payment model

### API Endpoints

- [x] Create InternalOrganizationBankAccount (SuperUser)
- [x] Update InternalOrganizationBankAccount type (SuperUser)
- [x] Delete InternalOrganizationBankAccount (SuperUser)
- [x] Create ExternalOrganizationBankAccount using Plaid (Org Admin)
- [x] View payments list (Org Admin)
- [x] Create ACH debit payment (SuperUser)
- [x] View payment status

### Plaid Integration

- [x] Plaid Link setup
- [x] Create link token endpoint
- [x] Exchange public token endpoint
- [x] Account creation from Plaid data

## Frontend Requirements (Pending)

### Setup

- [ ] Next.js with TypeScript setup
- [ ] Pages Router implementation
- [ ] Project structure setup

### Components

- [ ] Plaid Link integration
- [ ] Bank account management interface
- [ ] Payment list view
- [ ] Payment status view

### Styling

- [ ] Modern UI implementation
- [ ] Responsive design
- [ ] Flexbox/Grid layouts

## Testing Requirements

- [ ] Backend unit tests
- [ ] Frontend component tests
- [ ] Integration tests
- [ ] Payment processing tests

## Documentation

- [x] Backend README with setup instructions
- [x] API documentation
- [ ] Frontend README
- [x] Environment variables documentation

## Repository Management

- [x] GitHub repository setup
- [x] Proper commit history with descriptive messages
- [x] Add team members as viewers:
  - [x] kaleb@jawntpass.com
  - [x] garrett@jawntpass.com
  - [x] nolan@jawntpass.com
  - [x] allie@jawntpass.com

## Notes

- Authentication/Authorization can be skipped (not required for assessment)
- Focus on demonstrating understanding of concepts
- Time management is important (Frontend: 60min, Backend: 90min)
- Comments can be used to "handwave" non-critical features
