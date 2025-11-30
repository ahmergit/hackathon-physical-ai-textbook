/**
 * Google OAuth Callback Page
 * This page is only shown if there's an error.
 * Successful OAuth redirects directly to /profile from the backend.
 */

import React, { useEffect, useState } from 'react';
import Layout from '@theme/Layout';
import styles from '../../auth.module.css';

export default function GoogleCallback() {
  const [message, setMessage] = useState('Processing Google sign-in...');

  useEffect(() => {
    // Check if there's an error in the URL (from backend redirect)
    const urlParams = new URLSearchParams(window.location.search);
    const error = urlParams.get('error');

    if (error) {
      setMessage(`Google sign-in failed: ${decodeURIComponent(error)}`);
    } else {
      // If we're here with a code, something went wrong
      // The backend should have handled the callback
      setMessage('Unexpected state. Please try signing in again.');
    }
  }, []);

  return (
    <Layout title="Google Sign-In" description="Processing Google authentication">
      <div className={styles.authContainer}>
        <div className={styles.authCard}>
          <h1>❌</h1>
          <h2>Sign-in Issue</h2>
          <p>{message}</p>
          <div style={{ marginTop: '1rem' }}>
            <a href="/physical-ai-humaniod-robotics/signup" className={styles.submitButton}>
              Try Again
            </a>
          </div>
        </div>
      </div>
    </Layout>
  );
}
