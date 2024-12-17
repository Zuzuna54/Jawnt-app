import Link from 'next/link';

export default function Home() {
    return (
        <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center bg-[var(--background)]">
            <div className="text-center px-4">
                <h1 className="text-4xl font-bold text-[var(--foreground)] mb-4">
                    Welcome to Jawnt Banking
                </h1>
                <p className="text-[var(--muted)] text-lg mb-8">
                    Manage your bank accounts and payments with ease
                </p>
                <div className="flex items-center justify-center gap-4">
                    <Link
                        href="/accounts"
                        className="btn btn-primary"
                    >
                        View Accounts
                    </Link>
                    <Link
                        href="/payments"
                        className="btn btn-primary"
                    >
                        View Payments
                    </Link>
                </div>
            </div>
        </div>
    );
}
