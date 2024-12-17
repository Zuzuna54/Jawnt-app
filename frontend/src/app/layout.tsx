import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Link from "next/link";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
    title: "Jawnt Banking",
    description: "Manage your bank accounts and payments",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body className={inter.className}>
                <nav className="bg-white shadow-sm">
                    <div className="container mx-auto px-4">
                        <div className="flex justify-between h-16">
                            <div className="flex">
                                <div className="flex-shrink-0 flex items-center">
                                    <span className="text-xl font-bold text-blue-600">Jawnt</span>
                                </div>
                                <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                                    <Link
                                        href="/accounts"
                                        className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900"
                                    >
                                        Accounts
                                    </Link>
                                    <Link
                                        href="/payments"
                                        className="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900"
                                    >
                                        Payments
                                    </Link>
                                </div>
                            </div>
                        </div>
                    </div>
                </nav>
                <main>{children}</main>
            </body>
        </html>
    );
}
