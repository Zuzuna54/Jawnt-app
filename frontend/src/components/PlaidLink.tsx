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
    const [isLoading, setIsLoading] = useState(false);

    const generateToken = useCallback(async () => {
        try {
            setIsLoading(true);
            setError(null);
            console.log('Generating Plaid link token...');
            const response = await axios.post('/api/v1/plaid/create-link-token', {
                user_id: 'test_user'
            });
            console.log('Link token generated:', response.data);
            setLinkToken(response.data.link_token);
        } catch (error) {
            console.error('Error generating link token:', error);
            setError('Failed to initialize Plaid Link');
        } finally {
            setIsLoading(false);
        }
    }, []);

    const onPlaidSuccess = useCallback(async (publicToken: string) => {
        try {
            setIsLoading(true);
            setError(null);
            console.log('Exchanging public token...');
            await axios.post('/api/v1/plaid/exchange-token', {
                public_token: publicToken,
                organization_id: organizationId
            });
            console.log('Token exchanged successfully');
            onSuccess();
        } catch (error) {
            console.error('Error exchanging token:', error);
            setError('Failed to link bank account');
        } finally {
            setIsLoading(false);
        }
    }, [organizationId, onSuccess]);

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
            <div className="space-y-4">
                <button
                    onClick={generateToken}
                    disabled={isLoading}
                    className="btn btn-secondary"
                >
                    {isLoading ? 'Retrying...' : 'Retry Connection'}
                </button>
                <p className="text-sm text-red-600">{error}</p>
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
            disabled={!ready || isLoading}
            className="btn btn-primary"
        >
            {isLoading ? (
                <span className="flex items-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Connecting...
                </span>
            ) : (
                'Connect Bank Account'
            )}
        </button>
    );
} 