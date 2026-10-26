'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from './AuthProvider';
import { getStoredUser } from '@/lib/auth';

interface ProtectedRouteProps {
  children: React.ReactNode;
  requiredRole?: 'college' | 'department';
}

export default function ProtectedRoute({ children, requiredRole }: ProtectedRouteProps) {
  const { user, loading, initialized } = useAuth();
  const router = useRouter();

  const activeUser = user || getStoredUser();

  useEffect(() => {
    if (initialized && !loading) {
      if (!activeUser) {
        // Not authenticated - redirect to login
        router.push('/login?redirect=' + encodeURIComponent(window.location.pathname));
        return;
      }

      if (requiredRole && activeUser.role) {
        const roleHierarchy: Record<string, number> = {
          'department': 1,
          'college': 2,
        };

        const userRoleLevel = roleHierarchy[activeUser.role] || 0;
        const requiredRoleLevel = roleHierarchy[requiredRole] || 0;

        if (userRoleLevel < requiredRoleLevel) {
          router.push('/unauthorized');
          return;
        }
      }
    }
  }, [activeUser, loading, initialized, requiredRole, router]);

  // Show loading state while checking credentials
  if (loading && !activeUser) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-4 border-primary border-t-transparent"></div>
      </div>
    );
  }

  // If completely unauthenticated, wait for redirect
  if (!activeUser) {
    return null;
  }

  // Check role if required
  if (requiredRole && activeUser.role) {
    const roleHierarchy: Record<string, number> = {
      'department': 1,
      'college': 2,
    };

    const userRoleLevel = roleHierarchy[activeUser.role] || 0;
    const requiredRoleLevel = roleHierarchy[requiredRole] || 0;

    if (userRoleLevel < requiredRoleLevel) {
      return null;
    }
  }

  return <>{children}</>;
}
