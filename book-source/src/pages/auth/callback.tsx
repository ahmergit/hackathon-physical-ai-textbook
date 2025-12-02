/**
 * OAuth Callback Page
 * Handles the return from Better Auth OAuth flow (Google, etc.)
 * Syncs user to FastAPI backend and redirects appropriately.
 */

import React, { useEffect, useState } from 'react';
import Layout from '@theme/Layout';
import { useAuth } from '../../contexts/AuthContext';
import styles from '../auth.module.css';

export default function AuthCallback() {
  const { user, isLoading } = useAuth();
  const [status, setStatus] = useState<'processing' | 'success' | 'error'>('processing');
  const [message, setMessage] = useState('Processing authentication...');

  useEffect(() => {
    const handleCallback = async () => {
      try {
        // Check for error in URL params
        const urlParams = new URLSearchParams(window.location.search);
        const error = urlParams.get('error');
        
        if (error) {
          setStatus('error');
          setMessage(`Authentication failed: ${decodeURIComponent(error)}`);
          return;
        }

        // Wait for auth state to update (AuthContext will auto-sync)
        await new Promise(resolve => setTimeout(resolve, 1500));

        // Check if we're now authenticated
        if (user) {
          setStatus('success');
          setMessage('Authentication successful! Redirecting...');
          
          // Redirect to profile/onboarding
          setTimeout(() => {
            window.location.href = '/physical-ai-humaniod-robotics/profile';
          }, 500);
        } else {
          // Wait a bit more for auth to complete
          await new Promise(resolve => setTimeout(resolve, 1500));
          
          // Final check - if still no user, show error
          if (!user) {
            setStatus('error');
            setMessage('Could not complete authentication. Please try again.');
          }
        }
      } catch (err: any) {
        console.error('Callback error:', err);
        setStatus('error');
        setMessage(err.message || 'An unexpected error occurred');
      }
    };

    if (!isLoading) {
      handleCallback();
    }
  }, [isLoading, user]);

  // If user is already set, redirect
  useEffect(() => {
    if (user && status === 'processing') {
      setStatus('success');
      setMessage('Already authenticated! Redirecting...');
      setTimeout(() => {
        window.location.href = '/physical-ai-humaniod-robotics/profile';
      }, 500);
    }
  }, [user, status]);

  return (
    <Layout title="Authentication" description="Processing authentication">
      <div className={styles.authContainer}>
        <div className={styles.authCard}>
          {status === 'processing' && (
            <>
              <h1>⏳</h1>
              <h2>Processing</h2>
              <p>{message}</p>
              <div style={{ marginTop: '1rem' }}>
                <div className={styles.spinner}></div>
              </div>
            </>
          )}
          
          {status === 'success' && (
            <>
              <h1>✅</h1>
              <h2>Success!</h2>
              <p>{message}</p>
            </>
          )}
          
          {status === 'error' && (
            <>
              <h1>❌</h1>
              <h2>Authentication Failed</h2>
              <p>{message}</p>
              <div style={{ marginTop: '1rem' }}>
                <a href="/physical-ai-humaniod-robotics/signup" className={styles.submitButton}>
                  Try Again
                </a>
              </div>
            </>
          )}
        </div>
      </div>
    </Layout>
  );
}
