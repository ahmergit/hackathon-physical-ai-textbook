/**
 * Onboarding page for collecting user profile information (one-time only)
 */

import React, { useState, useEffect } from 'react';
import Layout from '@theme/Layout';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { profileAPI, SkillLevel, DeviceType } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import styles from './auth.module.css';

// Validation schema - 4 fields for Better Auth migration
const onboardingSchema = z.object({
  hardware_skill: z.nativeEnum(SkillLevel),
  programming_skill: z.nativeEnum(SkillLevel),
  ai_ml_skill: z.nativeEnum(SkillLevel),
  current_device: z.nativeEnum(DeviceType),
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
      hardware_skill: SkillLevel.BEGINNER,
      programming_skill: SkillLevel.BEGINNER,
      ai_ml_skill: SkillLevel.BEGINNER,
      current_device: DeviceType.CLOUD_LAPTOP,
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
            Tell us about your experience and setup
          </p>

          <form onSubmit={handleSubmit(onSubmit)} className={styles.authForm}>
            <div className={styles.formGroup}>
              <label htmlFor="hardware_skill">
                Hardware/Robotics Experience *
              </label>
              <select
                id="hardware_skill"
                {...register('hardware_skill')}
                className={errors.hardware_skill ? styles.inputError : ''}
              >
                <option value={SkillLevel.BEGINNER}>Beginner</option>
                <option value={SkillLevel.INTERMEDIATE}>Intermediate</option>
                <option value={SkillLevel.EXPERT}>Expert</option>
              </select>
              {errors.hardware_skill && (
                <span className={styles.errorText}>
                  {errors.hardware_skill.message}
                </span>
              )}
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="programming_skill">
                Programming Experience *
              </label>
              <select
                id="programming_skill"
                {...register('programming_skill')}
                className={errors.programming_skill ? styles.inputError : ''}
              >
                <option value={SkillLevel.BEGINNER}>Beginner</option>
                <option value={SkillLevel.INTERMEDIATE}>Intermediate</option>
                <option value={SkillLevel.EXPERT}>Expert</option>
              </select>
              {errors.programming_skill && (
                <span className={styles.errorText}>
                  {errors.programming_skill.message}
                </span>
              )}
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="ai_ml_skill">
                AI/ML Experience *
              </label>
              <select
                id="ai_ml_skill"
                {...register('ai_ml_skill')}
                className={errors.ai_ml_skill ? styles.inputError : ''}
              >
                <option value={SkillLevel.BEGINNER}>Beginner</option>
                <option value={SkillLevel.INTERMEDIATE}>Intermediate</option>
                <option value={SkillLevel.EXPERT}>Expert</option>
              </select>
              {errors.ai_ml_skill && (
                <span className={styles.errorText}>
                  {errors.ai_ml_skill.message}
                </span>
              )}
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="current_device">
                Current Device/Setup *
              </label>
              <select
                id="current_device"
                {...register('current_device')}
                className={errors.current_device ? styles.inputError : ''}
              >
                <option value={DeviceType.CLOUD_LAPTOP}>Cloud/Laptop (No GPU)</option>
                <option value={DeviceType.RTX_GPU}>RTX GPU Workstation</option>
                <option value={DeviceType.PHYSICAL_ROBOT}>Physical Robot</option>
              </select>
              {errors.current_device && (
                <span className={styles.errorText}>
                  {errors.current_device.message}
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
