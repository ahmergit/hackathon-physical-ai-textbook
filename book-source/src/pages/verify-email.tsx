/**
 * Email verification page that handles email verification callback
 */

import React, { useEffect, useState } from 'react';
import Layout from '@theme/Layout';
import { authAPI } from '../services/api';
import styles from './auth.module.css';

export default function VerifyEmail(): JSX.Element {
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('');
  const [email, setEmail] = useState('');

  useEffect(() => {
    const verifyToken = async () => {
      // Get token from URL query parameter
      const params = new URLSearchParams(window.location.search);
      const token = params.get('token');

      if (!token) {
        setStatus('error');
        setMessage('No verification token provided.');
        return;
      }

      try {
        const response = await authAPI.verifyEmail({ token });
        setStatus('success');
        setMessage(response.message);
        setEmail(response.email);

        // Redirect to login after 3 seconds
        setTimeout(() => {
          window.location.href = '/physical-ai-humaniod-robotics/login';
        }, 3000);
      } catch (err: any) {
        setStatus('error');
        setMessage(
          err.response?.data?.detail ||
            'Verification failed. The token may be invalid or expired.'
        );
      }
    };

    verifyToken();
  }, []);

  const handleResendClick = async () => {
    if (!email) {
      alert('Please provide your email address to resend verification.');
      return;
    }

    try {
      await authAPI.resendVerification({ email });
      alert('Verification email sent! Please check your inbox.');
    } catch (err: any) {
      alert('Failed to resend verification email. Please try again later.');
    }
  };

  return (
    <Layout title="Verify Email" description="Verify your email address">
      <div className={styles.authContainer}>
        <div className={styles.authCard}>
          {status === 'loading' && (
            <div style={{ textAlign: 'center' }}>
              <div className={styles.loadingSpinner}></div>
              <h2>Verifying Email...</h2>
              <p>Please wait while we verify your email address.</p>
            </div>
          )}

          {status === 'success' && (
            <div className={styles.successMessage}>
              <h2>✓ Email Verified!</h2>
              <p>{message}</p>
              <p>
                Your email <strong>{email}</strong> has been successfully
                verified.
              </p>
              <p>Redirecting to login page...</p>
            </div>
          )}

          {status === 'error' && (
            <div>
              <div className={styles.errorMessage}>
                <h2>Verification Failed</h2>
                <p>{message}</p>
              </div>

              <div style={{ marginTop: '2rem', textAlign: 'center' }}>
                <p>Didn't receive the email or token expired?</p>
                <button
                  onClick={handleResendClick}
                  className={styles.submitButton}
                  style={{ marginTop: '1rem' }}
                >
                  Resend Verification Email
                </button>
              </div>

              <div className={styles.authFooter}>
                <p>
                  <a href="/physical-ai-humaniod-robotics/signup">Back to Sign Up</a>
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}
