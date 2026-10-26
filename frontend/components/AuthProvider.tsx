'use client';

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { User as FirebaseUser, onAuthStateChanged, getIdToken } from 'firebase/auth';
import { auth } from '@/lib/firebase';
import { initializeAuth, getCurrentUser, getStoredUser, AuthUser } from '@/lib/auth';

interface AuthContextType {
  user: AuthUser | null;
  loading: boolean;
  initialized: boolean;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  loading: true,
  initialized: false,
});

export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }: { children: ReactNode }) {
  // Synchronously restore user from localStorage to eliminate any flicker or false logout
  const [user, setUser] = useState<AuthUser | null>(() => getStoredUser());
  const [loading, setLoading] = useState<boolean>(() => !getStoredUser());
  const [initialized, setInitialized] = useState<boolean>(() => !!getStoredUser());

  useEffect(() => {
    let mounted = true;

    // Check for cached local user immediately
    const cachedUser = getStoredUser();
    if (cachedUser && mounted) {
      setUser(cachedUser);
      setLoading(false);
      setInitialized(true);
    }

    // Run auth initialization in background to verify / refresh token
    initializeAuth()
      .then((authUser) => {
        if (mounted && authUser) {
          setUser(authUser);
        }
      })
      .catch((err) => {
        console.warn('initializeAuth background notice:', err);
      })
      .finally(() => {
        if (mounted) {
          setLoading(false);
          setInitialized(true);
        }
      });

    // Listen for Firebase auth state changes
    const unsubscribe = onAuthStateChanged(auth, async (firebaseUser: FirebaseUser | null) => {
      if (!mounted) return;

      if (firebaseUser) {
        // Firebase user signed in - update token & user info
        try {
          const freshToken = await getIdToken(firebaseUser);
          if (freshToken) {
            localStorage.setItem('auth_token', freshToken);
          }
        } catch (e) {
          console.warn('Could not refresh Firebase token:', e);
        }

        const storedUser = getStoredUser();
        if (storedUser) {
          setUser(storedUser);
        } else {
          setUser(getCurrentUser());
        }
      } else {
        // Firebase user is null.
        // DO NOT log out if there is a cached user or demo user in localStorage!
        const existing = getStoredUser();
        if (existing) {
          setUser(existing);
        } else {
          setUser(null);
        }
      }

      setLoading(false);
      setInitialized(true);
    });

    return () => {
      mounted = false;
      unsubscribe();
    };
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading, initialized }}>
      {children}
    </AuthContext.Provider>
  );
}
