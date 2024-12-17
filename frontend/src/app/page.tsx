import Link from 'next/link';

export default function Home() {
    return (
        <div className="container mx-auto px-4 py-16">
            <div className="max-w-2xl mx-auto text-center">
                <h1 className="text-4xl font-bold text-gray-900 mb-8">
                    Welcome to Jawnt Banking
                </h1>
                <p className="text-xl text-gray-600 mb-12">
                    Manage your bank accounts and payments with ease
                </p>
                <div className="space-x-4">
                    <Link
                        href="/accounts"
                        className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
                    >
                        View Accounts
                    </Link>
                    <Link
                        href="/payments"
                        className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-blue-600 bg-white border-blue-600 hover:bg-blue-50"
                    >
                        View Payments
                    </Link>
                </div>
            </div>
        </div>
    );
}
