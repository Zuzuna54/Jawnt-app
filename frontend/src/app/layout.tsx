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
        <html lang="en" suppressHydrationWarning>
            <body className={`${inter.className} bg-[var(--background)]`} suppressHydrationWarning>
                <nav className="bg-[var(--card-bg)] border-b border-[var(--border)] sticky top-0 z-10">
                    <div className="container mx-auto px-4">
                        <div className="flex h-16 items-center justify-between">
                            <div className="flex items-center space-x-8">
                                <Link href="/" className="text-xl font-semibold text-[var(--primary)]">
                                    Jawnt
                                </Link>
                                <div className="hidden md:flex items-center space-x-6">
                                    <Link
                                        href="/accounts"
                                        className="nav-link text-sm font-medium"
                                    >
                                        Accounts
                                    </Link>
                                    <Link
                                        href="/payments"
                                        className="nav-link text-sm font-medium"
                                    >
                                        Payments
                                    </Link>
                                </div>
                            </div>
                            <div className="flex items-center">
                                <span className="text-sm text-[var(--muted)]">Demo Account</span>
                            </div>
                        </div>
                    </div>
                </nav>
                <main>{children}</main>
            </body>
        </html>
    );
}
