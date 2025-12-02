import React, { useState, useRef, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import styles from './NavbarAuth.module.css';

type ModalMode = 'signup' | 'login';

export default function NavbarAuth() {
  const { user, isLoading, loginWithEmail, signupWithEmail, loginWithGoogle, logout } = useAuth();
  const [showDropdown, setShowDropdown] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [modalMode, setModalMode] = useState<ModalMode>('signup');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');
  
  // Form state
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowDropdown(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Close modal on escape key
  useEffect(() => {
    function handleEscape(event: KeyboardEvent) {
      if (event.key === 'Escape') {
        setShowModal(false);
      }
    }
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, []);

  // Listen for openAuthModal event from ChatBot
  useEffect(() => {
    function handleOpenAuthModal(event: CustomEvent<{ mode: 'login' | 'signup' }>) {
      setModalMode(event.detail?.mode || 'login');
      resetForm();
      setShowModal(true);
    }
    window.addEventListener('openAuthModal', handleOpenAuthModal as EventListener);
    return () => window.removeEventListener('openAuthModal', handleOpenAuthModal as EventListener);
  }, []);

  const resetForm = () => {
    setName('');
    setEmail('');
    setPassword('');
    setError('');
  };

  const openModal = (mode: ModalMode) => {
    setModalMode(mode);
    resetForm();
    setShowModal(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      if (modalMode === 'signup') {
        if (!name.trim()) {
          throw new Error('Name is required');
        }
        // Client-side password validation (Better Auth enforces min 8 chars)
        if (password.length < 8) {
          throw new Error('Password must be at least 8 characters');
        }
        await signupWithEmail(name, email, password);
        setShowModal(false);
        resetForm();
        // AuthContext will automatically redirect to onboarding if needed
      } else {
        await loginWithEmail(email, password);
        setShowModal(false);
        resetForm();
        // AuthContext will automatically redirect to onboarding if profile doesn't exist
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCloseModal = () => {
    setShowModal(false);
    resetForm();
  };

  const handleLogout = () => {
    logout();
    setShowDropdown(false);
  };

  const handleGoogleSignIn = async () => {
    // Use Better Auth Google OAuth (client-side initiation for proper state cookie)
    try {
      await loginWithGoogle();
    } catch (error) {
      console.error('Google sign-in error:', error);
    }
  };

  const getInitials = (name: string) => {
    return name
      .split(' ')
      .map(part => part[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  if (isLoading) {
    return null;
  }

  return (
    <div className={styles.authContainer}>
      {user ? (
        // Logged in - show user button with dropdown
        <div ref={dropdownRef} style={{ position: 'relative' }}>
          <button
            className={`${styles.authButton} ${styles.userButton}`}
            onClick={() => setShowDropdown(!showDropdown)}
            aria-expanded={showDropdown}
            aria-haspopup="true"
          >
            <span className={styles.userAvatar}>{getInitials(user.name)}</span>
            <span className={styles.userName}>{user.name}</span>
            <svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M2.5 4.5L6 8L9.5 4.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
          
          {showDropdown && (
            <div className={styles.dropdown}>
              <div className={styles.dropdownItem} style={{ borderBottom: '1px solid var(--ifm-color-emphasis-200)' }}>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                  <circle cx="12" cy="7" r="4" />
                </svg>
                <div>
                  <div style={{ fontWeight: 600 }}>{user.name}</div>
                  <div style={{ fontSize: '12px', opacity: 0.7 }}>{user.email}</div>
                </div>
              </div>
              <button className={`${styles.dropdownItem} ${styles.logoutItem}`} onClick={handleLogout}>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
                  <polyline points="16 17 21 12 16 7" />
                  <line x1="21" y1="12" x2="9" y2="12" />
                </svg>
                Logout
              </button>
            </div>
          )}
        </div>
      ) : (
        // Not logged in - show signup button
        <button
          className={`${styles.authButton} ${styles.signupButton}`}
          onClick={() => openModal('signup')}
        >
          Sign Up
        </button>
      )}

      {/* Auth Modal */}
      {showModal && (
        <div className={styles.modalOverlay} onClick={handleCloseModal}>
          <div className={styles.modal} onClick={e => e.stopPropagation()}>
            <div className={styles.modalHeader}>
              <h2 className={styles.modalTitle}>
                {modalMode === 'signup' ? 'Create Account' : 'Welcome Back'}
              </h2>
              <button className={styles.closeButton} onClick={handleCloseModal}>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="18" y1="6" x2="6" y2="18" />
                  <line x1="6" y1="6" x2="18" y2="18" />
                </svg>
              </button>
            </div>

            <form className={styles.form} onSubmit={handleSubmit}>
              {error && <div className={styles.error}>{error}</div>}
              
              {modalMode === 'signup' && (
                <div className={styles.inputGroup}>
                  <label className={styles.label} htmlFor="name">Name</label>
                  <input
                    id="name"
                    type="text"
                    className={styles.input}
                    placeholder="Enter your name"
                    value={name}
                    onChange={e => setName(e.target.value)}
                    required
                    autoFocus
                  />
                </div>
              )}
              
              <div className={styles.inputGroup}>
                <label className={styles.label} htmlFor="email">Email</label>
                <input
                  id="email"
                  type="email"
                  className={styles.input}
                  placeholder="Enter your email"
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                  required
                  autoFocus={modalMode === 'login'}
                />
              </div>
              
              <div className={styles.inputGroup}>
                <label className={styles.label} htmlFor="password">Password</label>
                <input
                  id="password"
                  type="password"
                  className={styles.input}
                  placeholder="Enter your password"
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  required
                  minLength={8}
                />
                {modalMode === 'signup' && (
                  <p className={styles.passwordHint}>
                    Min. 8 characters with uppercase, lowercase, and number
                  </p>
                )}
              </div>
              
              <button type="submit" className={styles.submitButton} disabled={isSubmitting}>
                {isSubmitting ? 'Please wait...' : (modalMode === 'signup' ? 'Sign Up' : 'Login')}
              </button>

              <div className={styles.divider}>
                <span>or</span>
              </div>

              <button
                type="button"
                className={styles.googleButton}
                onClick={handleGoogleSignIn}
              >
                <svg width="18" height="18" viewBox="0 0 24 24">
                  <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                  <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                  <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                  <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                </svg>
                Continue with Google
              </button>
            </form>

            <div className={styles.switchMode}>
              {modalMode === 'signup' ? (
                <>
                  Already have an account?
                  <button className={styles.switchButton} onClick={() => { setModalMode('login'); setError(''); }}>
                    Login
                  </button>
                </>
              ) : (
                <>
                  Don't have an account?
                  <button className={styles.switchButton} onClick={() => { setModalMode('signup'); setError(''); }}>
                    Sign Up
                  </button>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
