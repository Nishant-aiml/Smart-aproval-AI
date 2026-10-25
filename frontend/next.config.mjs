/** @type {import('next').NextConfig} */
const backendPort = (process.env.BACKEND_PORT || '8051').toString().trim();
const rawBackendUrl = process.env.BACKEND_URL ? process.env.BACKEND_URL.trim() : '';
const backendUrl = rawBackendUrl
  ? (rawBackendUrl.startsWith('http://') || rawBackendUrl.startsWith('https://')
      ? rawBackendUrl
      : `https://${rawBackendUrl}`).replace(/\/+$/, '')
  : `http://127.0.0.1:${backendPort}`;

const nextConfig = {
  reactStrictMode: false,
  swcMinify: true,

  // Allowed origins for development and cloud hosting
  allowedDevOrigins: [
    '*.ngrok-free.app',
    '*.ngrok-free.dev',
    '*.ngrok.app',
    '*.ngrok.dev',
    '*.onrender.com',
    'localhost:3050',
    'localhost:3051',
  ],

  experimental: {
    // Automatically tree-shakes lucide-react and recharts imports
    // Drastically reduces compilation overhead and route transition latency
    optimizePackageImports: ['lucide-react', 'recharts'],
  },

  env: {
    NEXT_PUBLIC_API_BASE: process.env.NEXT_PUBLIC_API_BASE || '/api',
  },

  // Reverse proxy API and docs requests to FastAPI backend
  // Supports both local development and Render/cloud deployment via BACKEND_URL
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${backendUrl}/api/:path*`,
      },
      {
        source: '/docs',
        destination: `${backendUrl}/docs`,
      },
      {
        source: '/openapi.json',
        destination: `${backendUrl}/openapi.json`,
      },
    ];
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
