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
            const [externalRes, internalRes] = await Promise.all([
                axios.get('/api/v1/external-accounts'),
                axios.get('/api/v1/internal-accounts')
            ]);
            setExternalAccounts(externalRes.data);
            setInternalAccounts(internalRes.data);
        } catch (error) {
            console.error('Error fetching accounts:', error);
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
        <div className="container mx-auto px-4 py-8">
            <h1 className="text-3xl font-bold mb-8">Bank Accounts</h1>

            <div className="mb-8">
                <h2 className="text-xl font-semibold mb-4">Connect External Account</h2>
                <PlaidLink
                    organizationId={1}
                    onSuccess={handlePlaidSuccess}
                    onExit={() => console.log('Plaid Link closed')}
                />
            </div>

            {loading ? (
                <div>Loading accounts...</div>
            ) : (
                <div className="grid md:grid-cols-2 gap-8">
                    <div>
                        <h2 className="text-xl font-semibold mb-4">External Accounts</h2>
                        {externalAccounts.length === 0 ? (
                            <p>No external accounts connected</p>
                        ) : (
                            <div className="space-y-4">
                                {externalAccounts.map((account) => (
                                    <div
                                        key={account.uuid}
                                        className="p-4 border rounded-lg shadow-sm"
                                    >
                                        <h3 className="font-medium">{account.bank_name}</h3>
                                        <p className="text-sm text-gray-600">
                                            Account: ****{account.account_number.toString().slice(-4)}
                                        </p>
                                        <p className="text-sm text-gray-600">
                                            Type: {account.account_type}
                                        </p>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>

                    <div>
                        <h2 className="text-xl font-semibold mb-4">Internal Accounts</h2>
                        {internalAccounts.length === 0 ? (
                            <p>No internal accounts available</p>
                        ) : (
                            <div className="space-y-4">
                                {internalAccounts.map((account) => (
                                    <div
                                        key={account.uuid}
                                        className="p-4 border rounded-lg shadow-sm"
                                    >
                                        <h3 className="font-medium">
                                            {account.type?.charAt(0).toUpperCase() + account.type?.slice(1)} Account
                                        </h3>
                                        <p className="text-sm text-gray-600">
                                            Account: ****{account.account_number.toString().slice(-4)}
                                        </p>
                                        <p className="text-sm text-gray-600">
                                            Type: {account.type}
                                        </p>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
} 