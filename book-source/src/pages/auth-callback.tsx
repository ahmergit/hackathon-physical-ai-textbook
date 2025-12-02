/**
 * OAuth Callback Handler
 *
 * Handles redirect after Google OAuth completes:
 * 1. Better Auth session is established (cookie set)
 * 2. Calls /api/sync-user to get JWT tokens
 * 3. Stores tokens in localStorage
 * 4. Redirects to /onboarding or home based on profile status
 */

import React, { useEffect, useState } from 'react';
import { useHistory } from '@docusaurus/router';
import axios from 'axios';
import Layout from '@theme/Layout';

// Helper to get auth service URL (browser-compatible)
const getAuthServiceUrl = () =>
  typeof process !== 'undefined' && process.env?.AUTH_SERVICE_URL
    ? process.env.AUTH_SERVICE_URL
    : 'http://localhost:3001';

export default function AuthCallback() {
  const history = useHistory();
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('Completing authentication...');

  useEffect(() => {
    const handleCallback = async () => {
      try {
        setStatus('loading');
        setMessage('Syncing your account...');

        // Call sync-user to get JWT tokens (session cookie automatically sent)
        const response = await axios.post(
          `${getAuthServiceUrl()}/api/sync-user`,
          {},
          { withCredentials: true }
        );

        const { accessToken, refreshToken, needsOnboarding, user } = response.data;

        // Store tokens
        localStorage.setItem('access_token', accessToken);
        localStorage.setItem('refresh_token', refreshToken);

        setStatus('success');
        setMessage(`Welcome, ${user.name}!`);

        // Redirect based on onboarding status
        setTimeout(() => {
          if (needsOnboarding) {
            history.push('/physical-ai-humaniod-robotics/onboarding');
          } else {
            history.push('/physical-ai-humaniod-robotics/');
          }
        }, 1000);

      } catch (error: any) {
        console.error('OAuth callback failed:', error);
        setStatus('error');
        setMessage(
          error.response?.data?.error ||
          'Authentication failed. Please try again.'
        );

        // Redirect to home after error
        setTimeout(() => {
          history.push('/physical-ai-humaniod-robotics/?error=auth_failed');
        }, 3000);
      }
    };

    handleCallback();
  }, [history]);

  return (
    <Layout title="Authentication">
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '60vh',
        padding: '2rem',
      }}>
        {status === 'loading' && (
          <>
            <div style={{
              width: '50px',
              height: '50px',
              border: '4px solid #f3f3f3',
              borderTop: '4px solid #3498db',
              borderRadius: '50%',
              animation: 'spin 1s linear infinite',
              marginBottom: '1rem',
            }} />
            <h2>{message}</h2>
          </>
        )}

        {status === 'success' && (
          <>
            <div style={{
              width: '60px',
              height: '60px',
              borderRadius: '50%',
              backgroundColor: '#4caf50',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: '1rem',
            }}>
              <span style={{ color: 'white', fontSize: '30px' }}>✓</span>
            </div>
            <h2>{message}</h2>
            <p>Redirecting...</p>
          </>
        )}

        {status === 'error' && (
          <>
            <div style={{
              width: '60px',
              height: '60px',
              borderRadius: '50%',
              backgroundColor: '#f44336',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: '1rem',
            }}>
              <span style={{ color: 'white', fontSize: '30px' }}>✗</span>
            </div>
            <h2>Authentication Failed</h2>
            <p>{message}</p>
          </>
        )}

        <style>{`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}</style>
      </div>
    </Layout>
  );
}
