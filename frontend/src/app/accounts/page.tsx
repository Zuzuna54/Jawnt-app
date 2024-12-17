'use client';

import { useState, useEffect } from 'react';
import { PlaidLink } from '@/components/PlaidLink';
import axios from 'axios';

interface BankAccount {
    id: number;
    uuid: string;
    account_number: number;
    routing_number: number;
    bank_name?: string;
    account_type?: string;
    type?: 'funding' | 'claims';
}

export default function AccountsPage() {
    const [externalAccounts, setExternalAccounts] = useState<BankAccount[]>([]);
    const [internalAccounts, setInternalAccounts] = useState<BankAccount[]>([]);
    const [loading, setLoading] = useState(true);

    const fetchAccounts = async () => {
        try {
            console.log('Fetching accounts...');
            const [externalRes, internalRes] = await Promise.all([
                axios.get('/api/v1/external-accounts'),
                axios.get('/api/v1/internal-accounts')
            ]);
            console.log('External accounts response:', externalRes);
            console.log('Internal accounts response:', internalRes);

            if (Array.isArray(externalRes.data)) {
                setExternalAccounts(externalRes.data);
            } else {
                console.error('External accounts response is not an array:', externalRes.data);
            }

            if (Array.isArray(internalRes.data)) {
                setInternalAccounts(internalRes.data);
            } else {
                console.error('Internal accounts response is not an array:', internalRes.data);
            }
        } catch (error: unknown) {
            console.error('Error fetching accounts:', {
                message: (error as Error).message,
                response: (error as unknown as { response?: { data: unknown; status: number } }).response?.data,
                status: (error as unknown as { response?: { status: number } }).response?.status
            });
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchAccounts();
    }, []);

    const handlePlaidSuccess = () => {
        fetchAccounts();
    };

    return (
        <div className="min-h-screen bg-[var(--background)]">
            <div className="container mx-auto px-4 py-8">
                <div className="max-w-6xl mx-auto">
                    <h1 className="text-2xl font-semibold text-[var(--foreground)] mb-8">Bank Accounts</h1>

                    <div className="card mb-8">
                        <div className="flex items-center justify-between mb-6">
                            <div>
                                <h2 className="text-lg font-medium text-[var(--foreground)]">Connect Bank Account</h2>
                                <p className="text-[var(--muted)] mt-1">
                                    Link your external bank account securely using Plaid to enable transfers and payments.
                                </p>
                            </div>
                            <PlaidLink
                                organizationId={1}
                                onSuccess={handlePlaidSuccess}
                                onExit={() => console.log('Plaid Link closed')}
                            />
                        </div>
                    </div>

                    {loading ? (
                        <div className="flex justify-center items-center h-40">
                            <div className="text-[var(--muted)]">Loading accounts...</div>
                        </div>
                    ) : (
                        <div className="grid lg:grid-cols-2 gap-6">
                            <div>
                                <h2 className="text-lg font-medium text-[var(--foreground)] mb-4">External Accounts</h2>
                                {externalAccounts.length === 0 ? (
                                    <div className="card border-dashed">
                                        <div className="flex flex-col items-center justify-center py-6">
                                            <p className="text-[var(--muted)] text-center">No external accounts connected</p>
                                        </div>
                                    </div>
                                ) : (
                                    <div className="space-y-4">
                                        {externalAccounts.map((account) => (
                                            <div key={account.uuid} className="card">
                                                <div className="flex items-center justify-between mb-3">
                                                    <h3 className="font-medium text-[var(--foreground)]">{account.bank_name}</h3>
                                                    <span className="badge badge-blue">
                                                        {account.account_type}
                                                    </span>
                                                </div>
                                                <p className="text-[var(--muted)] text-sm">
                                                    Account ending in {account.account_number.toString().slice(-4)}
                                                </p>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>

                            <div>
                                <h2 className="text-lg font-medium text-[var(--foreground)] mb-4">Internal Accounts</h2>
                                {internalAccounts.length === 0 ? (
                                    <div className="card border-dashed">
                                        <div className="flex flex-col items-center justify-center py-6">
                                            <p className="text-[var(--muted)] text-center">No internal accounts available</p>
                                        </div>
                                    </div>
                                ) : (
                                    <div className="space-y-4">
                                        {internalAccounts.map((account) => (
                                            <div key={account.uuid} className="card">
                                                <div className="flex items-center justify-between mb-3">
                                                    <h3 className="font-medium text-[var(--foreground)]">
                                                        {account.type ? account.type.charAt(0).toUpperCase() + account.type.slice(1) : ''} Account
                                                    </h3>
                                                    <span className="badge badge-green">
                                                        {account.type}
                                                    </span>
                                                </div>
                                                <p className="text-[var(--muted)] text-sm">
                                                    Account ending in {account.account_number.toString().slice(-4)}
                                                </p>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
} 