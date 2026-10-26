'use client';

import { useEffect, useState } from 'react';
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
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const activeUser = user || (mounted ? getStoredUser() : null);

  useEffect(() => {
    if (mounted && initialized && !loading) {
      if (!activeUser) {
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
        }
      }
    }
  }, [mounted, activeUser, loading, initialized, requiredRole, router]);

  // Initial SSR and hydration pass renders spinner to ensure 100% server-client DOM parity
  if (!mounted || (loading && !activeUser) || !activeUser) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-4 border-primary border-t-transparent"></div>
      </div>
    );
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
