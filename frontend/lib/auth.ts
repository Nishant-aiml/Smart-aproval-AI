/**
 * Authentication Utilities
 * Handles Firebase Auth and backend token management
 */

import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signInWithPopup,
  GoogleAuthProvider,
  signOut as firebaseSignOut,
  User,
  onAuthStateChanged,
  getIdToken,
  getAdditionalUserInfo
} from 'firebase/auth';
import { auth } from './firebase';
import { api } from './api';

export interface AuthUser {
  uid: string;
  email: string | null;
  name: string | null;
  picture: string | null;
  role: string;
}

let currentUser: AuthUser | null = null;
let authToken: string | null = null;

// Google Auth Provider
const googleProvider = new GoogleAuthProvider();

// Optional: Add additional OAuth 2.0 scopes if needed
// googleProvider.addScope('https://www.googleapis.com/auth/contacts.readonly');

// Optional: Set custom OAuth parameters
// googleProvider.setCustomParameters({
//   'login_hint': 'user@example.com'
// });

/**
 * Sign in with email and password
 * Enhanced error handling following Firebase best practices
 */
export async function signInWithEmail(email: string, password: string): Promise<AuthUser> {
  try {
    const userCredential = await signInWithEmailAndPassword(auth, email, password);
    const idToken = await getIdToken(userCredential.user);
    return await loginToBackend(idToken);
  } catch (error: any) {
    // Handle specific Firebase Auth error codes
    const errorCode = error.code;

    if (errorCode === 'auth/user-not-found') {
      throw new Error('No account found with this email. Please sign up first.');
    } else if (errorCode === 'auth/wrong-password') {
      throw new Error('Incorrect password. Please try again.');
    } else if (errorCode === 'auth/invalid-email') {
      throw new Error('Invalid email address.');
    } else if (errorCode === 'auth/user-disabled') {
      throw new Error('This account has been disabled. Please contact support.');
    } else if (errorCode === 'auth/too-many-requests') {
      throw new Error('Too many failed attempts. Please try again later.');
    } else if (errorCode === 'auth/network-request-failed') {
      throw new Error('Network error. Please check your connection and try again.');
    }

    throw new Error(error.message || 'Failed to sign in');
  }
}

/**
 * Sign up with email and password
 */
export async function signUpWithEmail(email: string, password: string, name?: string, role: 'department' | 'college' = 'department'): Promise<AuthUser> {
  try {
    const userCredential = await createUserWithEmailAndPassword(auth, email, password);

    // Update display name if provided
    if (name && userCredential.user) {
      // Note: To update display name, you'd need to use updateProfile
      // For now, we'll just proceed with the sign up
    }

    const idToken = await getIdToken(userCredential.user);

    // Set role via backend (sets Firebase custom claims)
    try {
      await api.post('/auth/set-role', {
        id_token: idToken,
        role: role
      });
    } catch (roleError: any) {
      console.warn('Failed to set role, continuing with default:', roleError);
      // Continue even if role setting fails - backend will use default
    }

    // Get fresh token with custom claims
    const freshToken = await getIdToken(userCredential.user, true);
    return await loginToBackend(freshToken);
  } catch (error: any) {
    // Handle common Firebase errors
    if (error.code === 'auth/email-already-in-use') {
      throw new Error('This email is already registered. Please sign in instead.');
    } else if (error.code === 'auth/weak-password') {
      throw new Error('Password should be at least 6 characters.');
    } else if (error.code === 'auth/invalid-email') {
      throw new Error('Invalid email address.');
    }
    throw new Error(error.message || 'Failed to create account');
  }
}

/**
 * Sign in with Google using popup (simpler than redirect, no Firebase Hosting needed)
 * Returns the authenticated user directly
 */
export async function signInWithGoogle(role?: 'department' | 'college'): Promise<AuthUser> {
  try {
    const result = await signInWithPopup(auth, googleProvider);
    const user = result.user;
    const additionalInfo = getAdditionalUserInfo(result);

    // If this is a new user and role is provided, set the role
    if (additionalInfo?.isNewUser && role) {
      const idToken = await getIdToken(user);
      try {
        await api.post('/auth/set-role', {
          id_token: idToken,
          role: role
        });
        // Get fresh token with custom claims
        const freshToken = await getIdToken(user, true);
        return await loginToBackend(freshToken);
      } catch (roleError: any) {
        console.warn('Failed to set role, continuing with default:', roleError);
        return await loginToBackend(idToken);
      }
    }

    // Existing user or no role provided - just login
    const idToken = await getIdToken(user, true);
    return await loginToBackend(idToken);
  } catch (error: any) {
    // Handle Firebase Auth errors
    const errorCode = error.code;
    const errorMessage = error.message;

    if (errorCode === 'auth/popup-closed-by-user') {
      throw new Error('Sign-in cancelled. Please try again.');
    } else if (errorCode === 'auth/account-exists-with-different-credential') {
      throw new Error('An account already exists with the same email address but different sign-in credentials.');
    } else if (errorCode === 'auth/operation-not-allowed') {
      throw new Error('Google sign-in is not enabled. Please contact support.');
    } else if (errorCode === 'auth/unauthorized-domain') {
      throw new Error('This domain is not authorized for OAuth operations. Please add it to Firebase Console.');
    } else if (errorCode === 'auth/popup-blocked') {
      throw new Error('Popup was blocked by browser. Please allow popups for this site.');
    }

    console.error('Google sign-in error:', errorCode, errorMessage);
    throw new Error(errorMessage || 'Failed to sign in with Google. Please try again.');
  }
}

/**
 * Handle Google redirect result (kept for compatibility, returns null with popup approach)
 * @deprecated Use signInWithGoogle directly - it now returns the user
 */
export async function handleGoogleRedirectResult(): Promise<AuthUser | null> {
  // With popup auth, this is no longer needed - kept for compatibility
  return null;
}

/**
 * Login to backend with Firebase ID token
 */
async function loginToBackend(idToken: string): Promise<AuthUser> {
  try {
    const response = await api.post('/auth/login', { id_token: idToken });
    const { user, role } = response.data;

    currentUser = {
      uid: user.uid,
      email: user.email,
      name: user.name,
      picture: user.picture,
      role: role || 'department',
    };

    authToken = idToken;

    // Set auth header for all future requests
    api.defaults.headers.common['Authorization'] = `Bearer ${idToken}`;

    // Store in localStorage
    localStorage.setItem('auth_token', idToken);
    localStorage.setItem('auth_user', JSON.stringify(currentUser));

    return currentUser;
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Failed to login to backend');
  }
}

/**
 * Get user profile from backend (includes role)
 */
export async function getUserProfile(): Promise<{ uid: string; email: string; name: string | null; role: string | null }> {
  try {
    const token = localStorage.getItem('auth_token');
    if (!token) {
      throw new Error('No auth token');
    }

    const response = await api.get('/users/profile', {
      headers: { Authorization: `Bearer ${token}` }
    });

    return response.data;
  } catch (error: any) {
    throw new Error(error.response?.data?.detail || 'Failed to get user profile');
  }
}

/**
 * Sign out
 */
export async function signOut(): Promise<void> {
  try {
    if (!isDemoMode()) {
      await firebaseSignOut(auth);
    }
  } catch (error: any) {
    console.warn('Sign out warning:', error);
  } finally {
    currentUser = null;
    authToken = null;
    delete api.defaults.headers.common['Authorization'];
    delete api.defaults.headers.common['X-Demo-Mode'];
    localStorage.removeItem('auth_token');
    localStorage.removeItem('auth_user');
    localStorage.removeItem('demo_user');
  }
}

/**
 * Get current user
 */
export function getCurrentUser(): AuthUser | null {
  return currentUser;
}

/**
 * Get auth token
 */
export function getAuthToken(): string | null {
  return authToken;
}

/**
 * Check if user is authenticated
 */
export function isAuthenticated(): boolean {
  return currentUser !== null;
}

/**
 * Initialize auth state (restore from localStorage)
 * Only real Firebase authentication - no demo mode
 */
export async function initializeAuth(): Promise<AuthUser | null> {
  // Check for demo user first
  if (typeof window !== 'undefined') {
    const demoUser = localStorage.getItem('demo_user');
    if (demoUser) {
      try {
        const parsed = JSON.parse(demoUser);
        currentUser = parsed;
        authToken = localStorage.getItem('auth_token') || 'demo-token';
        api.defaults.headers.common['Authorization'] = `Bearer ${authToken}`;
        api.defaults.headers.common['X-Demo-Mode'] = 'true';
        return currentUser;
      } catch {
        localStorage.removeItem('demo_user');
      }
    }
  }

  // Check localStorage for regular auth
  const storedToken = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null;
  const storedUser = typeof window !== 'undefined' ? localStorage.getItem('auth_user') : null;

  if (storedToken && storedUser && !storedToken.startsWith('demo-')) {
    try {
      // Verify token is still valid
      const response = await api.get('/auth/verify', {
        headers: { Authorization: `Bearer ${storedToken}` }
      });

      if (response.data.valid) {
        currentUser = JSON.parse(storedUser);
        authToken = storedToken;
        api.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`;
        return currentUser;
      }
    } catch (error) {
      // Token invalid, clear storage
      localStorage.removeItem('auth_token');
      localStorage.removeItem('auth_user');
    }
  }

  // Listen for Firebase auth state changes
  return new Promise((resolve) => {
    onAuthStateChanged(auth, async (firebaseUser: User | null) => {
      if (firebaseUser) {
        try {
          const idToken = await getIdToken(firebaseUser);
          const user = await loginToBackend(idToken);
          resolve(user);
        } catch (error) {
          resolve(null);
        }
      } else {
        resolve(null);
      }
    });
  });
}

/**
 * Require authentication (throws if not authenticated)
 */
export function requireAuth(): AuthUser {
  if (!currentUser) {
    throw new Error('Authentication required');
  }
  return currentUser;
}

/**
 * Check if running in demo mode
 */
export function isDemoMode(): boolean {
  if (typeof window === 'undefined') return false;
  return localStorage.getItem('demo_user') !== null;
}

/**
 * Login with demo mode (bypasses Firebase authentication)
 * Creates a mock user session for exploring the platform
 */
export async function loginWithDemo(role: 'department' | 'college' = 'college'): Promise<AuthUser> {
  const demoUser: AuthUser = {
    uid: 'demo-user-' + Date.now(),
    email: role === 'college' ? 'reviewer@smartapproval.ai' : 'faculty@smartapproval.ai',
    name: role === 'college' ? 'College Reviewer' : 'Department Faculty',
    picture: null,
    role: role,
  };

  currentUser = demoUser;
  authToken = 'demo-token-' + Date.now();

  localStorage.setItem('demo_user', JSON.stringify(demoUser));
  localStorage.setItem('auth_user', JSON.stringify(demoUser));
  localStorage.setItem('auth_token', authToken);

  api.defaults.headers.common['Authorization'] = `Bearer ${authToken}`;
  api.defaults.headers.common['X-Demo-Mode'] = 'true';

  return demoUser;
}

/**
 * Get demo user
 */
export function getDemoUser(): AuthUser | null {
  if (typeof window === 'undefined') return null;
  const stored = localStorage.getItem('demo_user');
  if (stored) {
    try {
      return JSON.parse(stored);
    } catch {
      return null;
    }
  }
  return null;
}

/**
 * Exit demo mode
 */
export function exitDemoMode(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('demo_user');
  localStorage.removeItem('auth_user');
  localStorage.removeItem('auth_token');
  currentUser = null;
  authToken = null;
  delete api.defaults.headers.common['Authorization'];
  delete api.defaults.headers.common['X-Demo-Mode'];
}
