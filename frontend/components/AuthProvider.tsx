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
  // Start with clean initial state for SSR/client hydration parity
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [initialized, setInitialized] = useState<boolean>(false);

  useEffect(() => {
    let mounted = true;

    // Immediately restore cached local user upon client mount
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
        console.warn('initializeAuth notice:', err);
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
        // Only clear user if no local/demo user exists in localStorage
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
