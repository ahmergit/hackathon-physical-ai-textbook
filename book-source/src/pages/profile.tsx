/**
 * User profile page - redirects to home if profile already exists
 * Profile can only be set once during onboarding
 */

import React, { useEffect } from 'react';
import Layout from '@theme/Layout';
import { profileAPI } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import styles from './auth.module.css';

export default function Profile(): React.ReactElement {
  const { user, isLoading: authLoading } = useAuth();

  useEffect(() => {
    if (authLoading) return;
    
    if (!user) {
      // Not logged in - open auth modal and redirect to home
      window.dispatchEvent(new CustomEvent('openAuthModal', { detail: { mode: 'login' } }));
      window.location.href = '/physical-ai-humaniod-robotics/';
      return;
    }

    // Check if user has profile
    const checkProfile = async () => {
      try {
        await profileAPI.getProfile();
        // Profile exists - redirect to home (profile already completed)
        window.location.href = '/physical-ai-humaniod-robotics/';
      } catch (err: any) {
        if (err.response?.status === 404) {
          // No profile yet, redirect to onboarding
          window.location.href = '/physical-ai-humaniod-robotics/onboarding';
        } else {
          // Other error - redirect to home
          window.location.href = '/physical-ai-humaniod-robotics/';
        }
      }
    };

    checkProfile();
  }, [authLoading, user]);

  return (
    <Layout title="Profile" description="Your learning profile">
      <div className={styles.authContainer}>
        <div className={styles.authCard}>
          <div style={{ textAlign: 'center' }}>
            <div className={styles.loadingSpinner}></div>
            <p style={{ color: '#9ca3af' }}>Redirecting...</p>
          </div>
        </div>
      </div>
    </Layout>
  );
}
