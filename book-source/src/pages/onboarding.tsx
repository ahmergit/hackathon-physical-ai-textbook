/**
 * Onboarding page for collecting user profile information (one-time only)
 */

import React, { useState, useEffect } from 'react';
import Layout from '@theme/Layout';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { profileAPI, ExperienceLevel } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import styles from './auth.module.css';

// Validation schema - simplified to 2 questions
const onboardingSchema = z.object({
  ai_agents_experience: z.nativeEnum(ExperienceLevel),
  robotics_hardware_experience: z.nativeEnum(ExperienceLevel),
});

type OnboardingFormData = z.infer<typeof onboardingSchema>;

export default function Onboarding(): JSX.Element {
  const { user, isLoading: authLoading } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [isCheckingProfile, setIsCheckingProfile] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<OnboardingFormData>({
    resolver: zodResolver(onboardingSchema),
    defaultValues: {
      ai_agents_experience: ExperienceLevel.BEGINNER,
      robotics_hardware_experience: ExperienceLevel.BEGINNER,
    },
  });

  // Check if user already has a profile - if so, redirect to home
  useEffect(() => {
    if (authLoading) return;

    if (!user) {
      // Not logged in - redirect to home and show login
      window.dispatchEvent(new CustomEvent('openAuthModal', { detail: { mode: 'signup' } }));
      window.location.href = '/physical-ai-humaniod-robotics/';
      return;
    }

    const checkExistingProfile = async () => {
      try {
        await profileAPI.getProfile();
        // Profile already exists - redirect to home
        window.location.href = '/physical-ai-humaniod-robotics/';
      } catch (err: any) {
        if (err.response?.status === 404) {
          // No profile - show onboarding form
          setIsCheckingProfile(false);
        } else {
          // Other error - still show form
          setIsCheckingProfile(false);
        }
      }
    };

    checkExistingProfile();
  }, [authLoading, user]);

  const onSubmit = async (data: OnboardingFormData) => {
    setIsLoading(true);
    setError(null);

    try {
      await profileAPI.createProfile(data);

      // Redirect to home page after profile creation
      window.location.href = '/physical-ai-humaniod-robotics/';
    } catch (err: any) {
      setError(
        err.response?.data?.detail ||
          'Failed to save profile. Please try again.'
      );
    } finally {
      setIsLoading(false);
    }
  };

  // Show loading while checking auth or profile
  if (authLoading || isCheckingProfile) {
    return (
      <Layout title="Complete Your Profile" description="Tell us about yourself">
        <div className={styles.authContainer}>
          <div className={styles.authCard}>
            <div style={{ textAlign: 'center' }}>
              <div className={styles.loadingSpinner}></div>
              <p style={{ color: '#9ca3af' }}>Loading...</p>
            </div>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout title="Complete Your Profile" description="Tell us about yourself">
      <div className={styles.authContainer}>
        <div className={styles.authCard} style={{ maxWidth: '500px' }}>
          <h1>Welcome!</h1>
          <p className={styles.subtitle}>
            Tell us about your experience level
          </p>

          <form onSubmit={handleSubmit(onSubmit)} className={styles.authForm}>
            <div className={styles.formGroup}>
              <label htmlFor="ai_agents_experience">
                AI Agents Development Experience *
              </label>
              <select
                id="ai_agents_experience"
                {...register('ai_agents_experience')}
                className={errors.ai_agents_experience ? styles.inputError : ''}
              >
                <option value={ExperienceLevel.BEGINNER}>Beginner</option>
                <option value={ExperienceLevel.INTERMEDIATE}>Intermediate</option>
                <option value={ExperienceLevel.ADVANCED}>Advanced</option>
              </select>
              {errors.ai_agents_experience && (
                <span className={styles.errorText}>
                  {errors.ai_agents_experience.message}
                </span>
              )}
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="robotics_hardware_experience">
                Robotics / Hardware Experience *
              </label>
              <select
                id="robotics_hardware_experience"
                {...register('robotics_hardware_experience')}
                className={errors.robotics_hardware_experience ? styles.inputError : ''}
              >
                <option value={ExperienceLevel.BEGINNER}>Beginner</option>
                <option value={ExperienceLevel.INTERMEDIATE}>Intermediate</option>
                <option value={ExperienceLevel.ADVANCED}>Advanced</option>
              </select>
              {errors.robotics_hardware_experience && (
                <span className={styles.errorText}>
                  {errors.robotics_hardware_experience.message}
                </span>
              )}
            </div>

            {error && (
              <div className={styles.errorMessage}>
                <strong>Error:</strong> {error}
              </div>
            )}

            <button
              type="submit"
              disabled={isLoading}
              className={styles.submitButton}
            >
              {isLoading ? 'Saving...' : 'Complete Setup'}
            </button>
          </form>

          <div className={styles.authFooter}>
            <p>
              <small>* Required fields</small>
            </p>
          </div>
        </div>
      </div>
    </Layout>
  );
}
