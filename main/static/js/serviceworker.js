// var staticCacheName = 'djangopwa-v1';
 
// self.addEventListener('install', function(event) {
//   event.waitUntil(
//     caches.open(staticCacheName).then(function(cache) {
//       return cache.addAll([
//         '',
//       ]);
//     })
//   );
// });
 
// self.addEventListener('fetch', function(event) {
//   var requestUrl = new URL(event.request.url);
//     if (requestUrl.origin === location.origin) {
//       if ((requestUrl.pathname === '/')) {
//         event.respondWith(caches.match(''));
//         return;
//       }
//     }
//     event.respondWith(
//       caches.match(event.request).then(function(response) {
//         return response || fetch(event.request);
//       })
//     );
// });



var staticCacheName = 'djangopwa-v1';
var assetsToCache = [
  '/',
  '/static/css/styles.css', // example static files, update paths as needed
  '/static/js/main.js', // example static files, update paths as needed
  // Add other assets as needed
];

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(staticCacheName).then(function(cache) {
      return cache.addAll(assetsToCache);
    })
  );
});

self.addEventListener('fetch', function(event) {
  var requestUrl = new URL(event.request.url);
  
  // Handle requests for static assets
  if (requestUrl.origin === location.origin) {
    if (requestUrl.pathname === '/') {
      event.respondWith(caches.match('/'));
      return;
    }
  }

  // Fetch from cache or network
  event.respondWith(
    caches.match(event.request).then(function(response) {
      return response || fetch(event.request);
    })
  );
});

// Optionally, add an activate event to clean up old caches
self.addEventListener('activate', function(event) {
  var cacheWhitelist = [staticCacheName];
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.map(function(cacheName) {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});


if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/service-worker.js').then(function(registration) {
    console.log('Service Worker registered with scope:', registration.scope);
  }).catch(function(error) {
    console.log('Service Worker registration failed:', error);
  });
}