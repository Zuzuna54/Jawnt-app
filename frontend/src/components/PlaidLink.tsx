import { useState, useCallback } from 'react';
import { usePlaidLink } from 'react-plaid-link';
import axios from 'axios';

interface PlaidLinkProps {
    organizationId: number;
    onSuccess: () => void;
    onExit: () => void;
}

export function PlaidLink({ organizationId, onSuccess, onExit }: PlaidLinkProps) {
    const [linkToken, setLinkToken] = useState<string | null>(null);

    // Get link token when component mounts
    const generateToken = useCallback(async () => {
        try {
            const response = await axios.post('http://localhost:8001/api/v1/plaid/create-link-token', {
                user_id: 'test_user' // In a real app, this would be the actual user ID
            });
            setLinkToken(response.data.link_token);
        } catch (error) {
            console.error('Error generating link token:', error);
        }
    }, []);

    const onPlaidSuccess = useCallback(async (publicToken: string) => {
        try {
            await axios.post('http://localhost:8001/api/v1/plaid/exchange-token', {
                public_token: publicToken,
                organization_id: organizationId
            });
            onSuccess();
        } catch (error) {
            console.error('Error exchanging token:', error);
        }
    }, [organizationId, onSuccess]);

    const { open, ready } = usePlaidLink({
        token: linkToken ?? '',
        onSuccess: (public_token) => {
            onPlaidSuccess(public_token);
        },
        onExit: () => {
            onExit();
        },
    });

    return (
        <button
            onClick={() => {
                if (!linkToken) {
                    generateToken();
                } else {
                    open();
                }
            }}
            disabled={!ready}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
        >
            Connect Bank Account
        </button>
    );
} 