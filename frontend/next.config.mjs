/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: false,
  swcMinify: true,

  experimental: {
    // Automatically tree-shakes lucide-react and recharts imports
    // Drastically reduces compilation overhead and route transition latency
    optimizePackageImports: ['lucide-react', 'recharts'],
  },

  env: {
    NEXT_PUBLIC_API_BASE: process.env.NEXT_PUBLIC_API_BASE || 'http://127.0.0.1:8000/api',
  },

  poweredByHeader: false,

  // Allow Firebase Google Auth popup window.closed communication without COOP restriction
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'Cross-Origin-Opener-Policy',
            value: 'unsafe-none',
          },
        ],
      },
    ];
  },

  images: {
    unoptimized: true,
  },

  // Skip ESLint during production builds for faster deployment
  eslint: {
    ignoreDuringBuilds: true,
  },

  // Skip TypeScript type checking during build (handled by IDE)
  typescript: {
    ignoreBuildErrors: true,
  },
};

export default nextConfig;
