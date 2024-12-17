# Jawnt Frontend

Modern Next.js frontend for the Jawnt banking application, featuring Plaid integration and real-time payment tracking.

## Features

### Bank Account Management

- **External Account Connection**

  - Plaid Link integration
  - Account type validation
  - Real-time status updates
  - Error handling

- **Account Display**
  - Internal account listing
  - External account listing
  - Account details
  - Type-based filtering

### Payment Processing

- **Payment Creation**

  - ACH debit initiation
  - ACH credit initiation
  - Book payment creation
  - Amount validation

- **Payment Tracking**
  - Status monitoring
  - Payment history
  - Transaction details
  - Error handling

### User Interface

- **Modern Design**

  - Responsive layout
  - Dark mode support
  - Loading states
  - Error states

- **Navigation**
  - Intuitive routing
  - Breadcrumb navigation
  - Active state handling
  - Mobile responsiveness

## Tech Stack

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Hooks
- **API Integration**: Axios
- **Banking Integration**: Plaid Link SDK

## Project Structure

```
src/
├── app/                    # Next.js 14 app directory
│   ├── accounts/          # Account management page
│   ├── payments/          # Payment tracking page
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # Reusable components
│   ├── PlaidLink.tsx     # Plaid integration
│   ├── AccountList.tsx   # Account display
│   └── PaymentForm.tsx   # Payment creation
├── hooks/                # Custom React hooks
│   ├── usePlaid.ts      # Plaid integration logic
│   └── usePayments.ts   # Payment management
├── lib/                  # Utility functions
│   ├── api.ts           # API client
│   └── utils.ts         # Helper functions
└── types/               # TypeScript definitions
    ├── accounts.ts      # Account types
    └── payments.ts      # Payment types
```

## Implementation Details

### Plaid Integration

```typescript
interface PlaidLinkProps {
  organizationId: number;
  onSuccess: () => void;
  onExit: () => void;
}

export function PlaidLink({
  organizationId,
  onSuccess,
  onExit,
}: PlaidLinkProps) {
  const [linkToken, setLinkToken] = useState<string | null>(null);
  const { open, ready } = usePlaidLink({
    token: linkToken ?? "",
    onSuccess: handleSuccess,
    onExit: handleExit,
  });
  // ... implementation
}
```

### Payment Management

```typescript
interface Payment {
  id: number;
  uuid: string;
  amount: number;
  status: "PENDING" | "SUCCESS" | "FAILURE";
  payment_type: "ACH_DEBIT" | "ACH_CREDIT" | "BOOK";
}

function PaymentList() {
  const [payments, setPayments] = useState<Payment[]>([]);
  const [loading, setLoading] = useState(true);
  // ... implementation
}
```

### Account Display

```typescript
interface BankAccount {
  id: number;
  uuid: string;
  account_number: number;
  routing_number: number;
  bank_name?: string;
  account_type?: string;
}

function AccountDisplay({ account }: { account: BankAccount }) {
  // ... implementation
}
```

## Getting Started

### Prerequisites

- Node.js 18 or higher
- pnpm package manager

### Installation

1. Install dependencies:

```bash
pnpm install
```

2. Set up environment variables:

```bash
cp .env.example .env.local
```

3. Start the development server:

```bash
pnpm dev
```

The application will be available at `http://localhost:3000`

## Available Scripts

- `pnpm dev` - Start development server
- `pnpm build` - Build production bundle
- `pnpm start` - Start production server
- `pnpm lint` - Run ESLint
- `pnpm type-check` - Run TypeScript type checking

## Component Documentation

### PlaidLink Component

The main component for integrating with Plaid Link:

```typescript
interface PlaidLinkProps {
  organizationId: number;
  onSuccess: () => void;
  onExit: () => void;
}
```

Usage:

```tsx
<PlaidLink organizationId={1} onSuccess={handleSuccess} onExit={handleExit} />
```

### Pages

- `/` - Home page with navigation to main features
- `/accounts` - Bank account management
- `/payments` - Payment history and tracking

## Styling

The application uses Tailwind CSS with a custom configuration:

```typescript
// tailwind.config.ts
export default {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "var(--primary)",
        background: "var(--background)",
        // ... other custom colors
      },
    },
  },
};
```

### Custom Theme

```css
:root {
  --primary: #0066f5;
  --background: #f7f9fc;
  --card-bg: #ffffff;
  --foreground: #1a2b4b;
  --muted: #64748b;
}

@media (prefers-color-scheme: dark) {
  :root {
    --background: #0f172a;
    --card-bg: #1e293b;
    // ... dark mode colors
  }
}
```

## API Integration

The frontend communicates with the backend through a RESTful API:

```typescript
// lib/api.ts
const api = axios.create({
  baseURL: "/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

export const createPayment = async (payment: PaymentCreate) => {
  const response = await api.post(`/payments/${payment.type}`, payment);
  return response.data;
};
```

## Best Practices

- TypeScript for type safety
- Component composition
- Responsive design principles
- Error boundary implementation
- Loading state management
- Clean code principles

## Error Handling

```typescript
try {
  const response = await api.post("/payments/ach-debit", payment);
  // Handle success
} catch (error) {
  if (axios.isAxiosError(error)) {
    // Handle API errors
  } else {
    // Handle other errors
  }
}
```

## Future Improvements

1. Add unit tests for components
2. Implement E2E testing
3. Add error tracking
4. Enhance accessibility
5. Add performance monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is part of a technical assessment and is not licensed for public use.
