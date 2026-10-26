'use client';

import { useState, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { signInWithEmail, signUpWithEmail, signInWithGoogle, getUserProfile, loginWithDemo } from '@/lib/auth';
import toast from 'react-hot-toast';
import { Mail, Lock, LogIn, Sparkles, ShieldCheck } from 'lucide-react';
import Link from 'next/link';

function LoginPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const redirect = searchParams.get('redirect') || '/';

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  // Check role and redirect accordingly
  const handleSuccessfulLogin = async () => {
    try {
      const profile = await getUserProfile();
      if (!profile.role) {
        window.location.href = `/select-role?redirect=${encodeURIComponent(redirect)}`;
      } else {
        if (profile.role === 'college') {
          window.location.href = '/';
        } else if (profile.role === 'department') {
          window.location.href = '/nba-dashboard';
        } else {
          window.location.href = redirect;
        }
      }
    } catch {
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
      // If user account is not found in Firebase, attempt auto-signup
      const isNotFound = 
        error.code === 'auth/user-not-found' || 
        error.code === 'auth/invalid-credential' ||
        error.message?.includes('No account found');

      if (isNotFound) {
        try {
          toast.loading('Creating new account for this email...', { id: 'auth-toast' });
          await signUpWithEmail(email, password, email.split('@')[0], 'college');
          toast.success('Account created & signed in!', { id: 'auth-toast' });
          await handleSuccessfulLogin();
          return;
        } catch (signupErr: any) {
          toast.dismiss('auth-toast');
          toast.error(signupErr.message || 'Login failed');
        }
      } else {
        toast.error(error.message || 'Login failed');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleDemoLogin = (role: 'college' | 'department') => {
    loginWithDemo(role);
    toast.success(`Signed in as ${role === 'college' ? 'College Reviewer' : 'Department Faculty'}`);
    if (role === 'college') {
      window.location.href = '/';
    } else {
      window.location.href = '/nba-dashboard';
    }
  };

  const handleGoogleLogin = async () => {
    setLoading(true);

    try {
      const user = await signInWithGoogle();
      toast.success('Google login successful!');

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
      const isUnauthorizedDomain = 
        error.code === 'auth/unauthorized-domain' || 
        error.message?.includes('not authorized for OAuth') ||
        error.message?.includes('Authorized Domains');

      if (isUnauthorizedDomain) {
        toast.error('Ngrok domain not yet added to Firebase OAuth domains. Auto-logging in as Reviewer...');
        setTimeout(() => handleDemoLogin('college'), 1200);
      } else {
        toast.error(error.message || 'Google login failed');
      }
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-3xl shadow-soft-xl p-8 border border-gray-100">
        {/* Header */}
        <div className="text-center mb-6">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 bg-primary-50 text-primary rounded-full text-xs font-semibold mb-3">
            <Sparkles className="w-3.5 h-3.5" /> Accreditation AI Platform
          </div>
          <h1 className="text-3xl font-bold text-gray-800 mb-1">
            Smart Approval <span className="text-primary">AI</span>
          </h1>
          <p className="text-sm text-gray-500">Sign in to access evaluations & dashboards</p>
        </div>

        {/* 1-Click Instant Reviewer Access */}
        <div className="mb-6 p-3.5 bg-gradient-to-r from-primary-50/80 to-secondary-50/80 rounded-2xl border border-primary-100/60">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold uppercase tracking-wider text-primary-dark flex items-center gap-1">
              <ShieldCheck className="w-4 h-4 text-primary" /> Instant Reviewer Access
            </span>
            <span className="text-[10px] bg-white px-2 py-0.5 rounded-full text-gray-500 font-medium border border-gray-200">
              No Password Needed
            </span>
          </div>
          <div className="grid grid-cols-2 gap-2">
            <button
              type="button"
              onClick={() => handleDemoLogin('college')}
              className="py-2.5 px-3 bg-white hover:bg-primary-50 text-primary hover:text-primary-dark border border-primary-200 rounded-xl text-xs font-bold transition-all shadow-sm text-center"
            >
              🏛️ College Admin
            </button>
            <button
              type="button"
              onClick={() => handleDemoLogin('department')}
              className="py-2.5 px-3 bg-white hover:bg-secondary-50 text-secondary hover:text-secondary-dark border border-secondary-200 rounded-xl text-xs font-bold transition-all shadow-sm text-center"
            >
              📚 NBA Dept Faculty
            </button>
          </div>
        </div>

        <div className="relative mb-5">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-200"></div>
          </div>
          <div className="relative flex justify-center text-xs">
            <span className="px-3 bg-white text-gray-400 font-medium">Or Sign In with Email / Firebase</span>
          </div>
        </div>

        {/* Email/Password Form */}
        <form onSubmit={handleEmailLogin} className="space-y-3.5 mb-5">
          <div>
            <label className="block text-xs font-semibold text-gray-700 mb-1.5">
              Email Address
            </label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full pl-9 pr-3.5 py-2.5 text-sm border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
                placeholder="reviewer@institution.edu"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-gray-700 mb-1.5">
              Password
            </label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full pl-9 pr-3.5 py-2.5 text-sm border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
                placeholder="••••••••"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-primary text-white py-2.5 rounded-xl text-sm font-semibold hover:bg-primary-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-sm"
          >
            {loading ? (
              <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
            ) : (
              <>
                <LogIn className="w-4 h-4" />
                Sign In
              </>
            )}
          </button>
        </form>

        {/* Google Sign In */}
        <button
          onClick={handleGoogleLogin}
          disabled={loading}
          className="w-full border border-gray-200 text-gray-700 py-2.5 rounded-xl text-sm font-semibold hover:bg-gray-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          <svg className="w-4 h-4" viewBox="0 0 24 24">
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

        {/* Footer */}
        <p className="text-center text-xs text-gray-500 mt-5">
          Don't have an account?{' '}
          <Link href="/signup" className="text-primary hover:underline font-semibold">
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
