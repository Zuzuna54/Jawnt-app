import { useState, useCallback, useEffect } from 'react';
import { usePlaidLink } from 'react-plaid-link';
import axios from 'axios';

interface PlaidLinkProps {
    organizationId: number;
    onSuccess: () => void;
    onExit: () => void;
}

export function PlaidLink({ organizationId, onSuccess, onExit }: PlaidLinkProps) {
    const [linkToken, setLinkToken] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);

    // Get link token when component mounts
    const generateToken = useCallback(async () => {
        try {
            console.log('Generating Plaid link token...');
            const response = await axios.post('/api/v1/plaid/create-link-token', {
                user_id: 'test_user'
            });
            console.log('Link token generated:', response.data);
            setLinkToken(response.data.link_token);
            setError(null);
        } catch (error) {
            console.error('Error generating link token:', error);
            setError('Failed to initialize Plaid Link');
        }
    }, []);

    const onPlaidSuccess = useCallback(async (publicToken: string) => {
        try {
            console.log('Exchanging public token...');
            await axios.post('/api/v1/plaid/exchange-token', {
                public_token: publicToken,
                organization_id: organizationId
            });
            console.log('Token exchanged successfully');
            onSuccess();
            setError(null);
        } catch (error) {
            console.error('Error exchanging token:', error);
            setError('Failed to link bank account');
        }
    }, [organizationId, onSuccess]);

    // Generate token on mount
    useEffect(() => {
        if (!linkToken) {
            generateToken();
        }
    }, [linkToken, generateToken]);

    const { open, ready } = usePlaidLink({
        token: linkToken ?? '',
        onSuccess: (public_token) => {
            console.log('Plaid Link success');
            onPlaidSuccess(public_token);
        },
        onExit: () => {
            console.log('Plaid Link closed');
            onExit();
        },
        onEvent: (eventName, metadata) => {
            console.log('Plaid Link event:', eventName, metadata);
        },
    });

    if (error) {
        return (
            <div>
                <button
                    onClick={generateToken}
                    className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
                >
                    Retry Connection
                </button>
                <p className="mt-2 text-sm text-red-600">{error}</p>
            </div>
        );
    }

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