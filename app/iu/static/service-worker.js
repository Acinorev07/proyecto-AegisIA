self.addEventListener('install', (event) => {
    self.skipWaiting();
    console.log('Service Worker instalado.');
  });
  
  self.addEventListener('activate', (event) => {
    console.log('Service Worker activado.');
  });
  
  self.addEventListener('fetch', (event) => {
    // Filtra las solicitudes que deseas interceptar
      console.log('Interceptando solicitud de red hacia:', event);
    
  
    event.respondWith(fetch(event.request));
  });
  

