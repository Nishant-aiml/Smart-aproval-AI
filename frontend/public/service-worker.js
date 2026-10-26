// Development & Production Service Worker
const CACHE_NAME = 'smart-approval-v3';

self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  // Clear old caches
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const url = event.request.url;

  // Never intercept dynamic APIs, HMR bundles, auth, or ngrok tunnels
  const skipKeywords = [
    '/api/',
    '/_next/',
    'googleapis.com',
    'firebase',
    'identitytoolkit',
    'securetoken',
    'accounts.google.com',
    'localhost',
    '127.0.0.1',
    'ngrok'
  ];

  if (skipKeywords.some(kw => url.includes(kw))) {
    return;
  }

  // Network-first strategy for static assets
  event.respondWith(
    fetch(event.request)
      .then((response) => response)
      .catch(async () => {
        const cachedResponse = await caches.match(event.request);
        if (cachedResponse) {
          return cachedResponse;
        }
        return new Response('Network error', {
          status: 408,
          statusText: 'Request Timeout',
          headers: new Headers({ 'Content-Type': 'text/plain' })
        });
      })
  );
});
