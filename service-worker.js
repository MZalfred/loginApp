const CACHE_NAME = 'fit-shirts-cache-v1';
const urlsToCache = [
  '/',
  '/styles.css',
  '/script.js'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                if (response) {
                    // Return cached asset
                    return response;
                }
                // Fetch from network if not available in cache
                return fetch(event.request);
            })
    );
});
