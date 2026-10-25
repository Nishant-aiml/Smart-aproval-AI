'use client';

import { useState, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { signInWithEmail, signInWithGoogle, getUserProfile, loginWithDemo } from '@/lib/auth';
import toast from 'react-hot-toast';
import { Mail, Lock, LogIn } from 'lucide-react';
import Link from 'next/link';

function LoginPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const redirect = searchParams.get('redirect') || '/';

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  // No need for redirect handling with popup auth

  // Check role and redirect accordingly
  const handleSuccessfulLogin = async () => {
    try {
      const profile = await getUserProfile();
      if (!profile.role) {
        // No role set - redirect to role selection (hard redirect)
        window.location.href = `/select-role?redirect=${encodeURIComponent(redirect)}`;
      } else {
        // Has role - redirect to role-specific dashboard (hard redirect)
        if (profile.role === 'college') {
          window.location.href = '/'; // College users go to main dashboard
        } else if (profile.role === 'department') {
          window.location.href = '/nba-dashboard'; // Department users go to NBA dashboard
        } else {
          window.location.href = redirect; // Fallback to original redirect
        }
      }
    } catch (error) {
      // If profile check fails, still redirect to dashboard (will be caught by protected route)
      window.location.href = redirect;
    }
  };

  const handleEmailLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      await signInWithEmail(email, password);
      toast.success('Login successful!');
      await handleSuccessfulLogin();
    } catch (error: any) {
      toast.error(error.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

    const handleDemoLogin = (role: 'college' | 'department') => {
    loginWithDemo(role);
    toast.success(`Entering demo mode as ${role === 'college' ? 'College Reviewer' : 'Department Faculty'}`);
    if (role === 'college') {
      window.location.href = '/';
    } else {
      window.location.href = '/nba-dashboard';
    }
  };

  const handleGoogleLogin = async () => {
    setLoading(true);

    try {
      // Popup-based sign in - returns user directly
      const user = await signInWithGoogle();
      toast.success('Login successful!');

      // Redirect based on user role
      if (!user.role || user.role === 'pending') {
        window.location.href = `/select-role?redirect=${encodeURIComponent(redirect)}`;
      } else if (user.role === 'college') {
        window.location.href = '/';
      } else if (user.role === 'department') {
        window.location.href = '/nba-dashboard';
      } else {
        window.location.href = redirect;
      }
    } catch (error: any) {
      toast.error(error.message || 'Google login failed');
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-3xl shadow-soft-xl p-8 border border-gray-100">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            Smart Approval <span className="text-primary">AI</span>
          </h1>
          <p className="text-gray-600">Sign in to continue</p>
        </div>

        {/* Email/Password Form */}
        <form onSubmit={handleEmailLogin} className="space-y-4 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email
            </label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent"
                placeholder="your@email.com"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Password
            </label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent"
                placeholder="••••••••"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-primary text-white py-3 rounded-xl font-semibold hover:bg-primary-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {loading ? (
              <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
            ) : (
              <>
                <LogIn className="w-5 h-5" />
                Sign In
              </>
            )}
          </button>
        </form>

        {/* Divider */}
        <div className="relative mb-6">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-200"></div>
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-4 bg-white text-gray-500">Or continue with</span>
          </div>
        </div>

        {/* Google Sign In */}
        <button
          onClick={handleGoogleLogin}
          disabled={loading}
          className="w-full border-2 border-gray-200 text-gray-700 py-3 rounded-xl font-semibold hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          <svg className="w-5 h-5" viewBox="0 0 24 24">
            <path
              fill="#4285F4"
              d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
            />
            <path
              fill="#34A853"
              d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
            />
            <path
              fill="#FBBC05"
              d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
            />
            <path
              fill="#EA4335"
              d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
            />
          </svg>
          Sign in with Google
        </button>

        {/* Instant Demo Access */}
        <div className="mt-6 pt-6 border-t border-gray-100">
          <p className="text-center text-xs font-semibold uppercase tracking-wider text-gray-500 mb-3">
            Quick Local Demo Access
          </p>
          <div className="grid grid-cols-2 gap-3">
            <button
              type="button"
              onClick={() => handleDemoLogin('college')}
              className="py-2.5 px-3 bg-primary/10 hover:bg-primary/20 text-primary border border-primary/20 rounded-xl text-xs font-semibold transition-all text-center"
            >
              🏛️ College View
            </button>
            <button
              type="button"
              onClick={() => handleDemoLogin('department')}
              className="py-2.5 px-3 bg-secondary/10 hover:bg-secondary/20 text-secondary border border-secondary/20 rounded-xl text-xs font-semibold transition-all text-center"
            >
              📚 NBA Dept View
            </button>
          </div>
        </div>

        {/* Footer */}
        <p className="text-center text-sm text-gray-500 mt-6">
          Don't have an account?{' '}
          <Link href="/signup" className="text-primary hover:underline font-medium">
            Sign up
          </Link>
        </p>
      </div>
    </div>
  );
}

export default function LoginPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-3 border-primary border-t-transparent" />
      </div>
    }>
      <LoginPageContent />
    </Suspense>
  );
}
