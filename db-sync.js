/* Conecta CampusConecta con los archivos JSON del servidor local. */
(async function () {
  const originalSet = Storage.prototype.setItem;
  const originalRemove = Storage.prototype.removeItem;
  let ready = false;
  try {
    const response = await fetch('/api/load', { cache: 'no-store' });
    if (response.ok) {
      const saved = await response.json();
      for (const [key, value] of Object.entries(saved)) {
        originalSet.call(localStorage, key, JSON.stringify(value));
      }
    }
    ready = true;
  } catch (error) {
    console.warn('No se pudo conectar con la base de datos en archivos. Ejecuta iniciar_campusconecta.bat.', error);
  }
  Storage.prototype.setItem = function (key, value) {
    originalSet.call(this, key, value);
    if (this === localStorage && ready && (String(key).startsWith('cc_'))) {
      let parsed = value;
      try { parsed = JSON.parse(value); } catch (_) {}
      fetch('/api/save', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ key: String(key), value: parsed })
      }).catch(err => console.error('No se pudo guardar en los archivos JSON:', err));
    }
  };
  Storage.prototype.removeItem = function (key) {
    originalRemove.call(this, key);
    if (this === localStorage && ready && String(key).startsWith('cc_')) {
      fetch('/api/save', { method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ key: String(key), value: null })
      }).catch(() => {});
    }
  };
  const script = document.createElement('script');
  script.src = location.pathname.endsWith('grupo.html') ? 'grupo.js' : 'app.js';
  document.body.appendChild(script);
})();
