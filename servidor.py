#!/usr/bin/env python3
"""Servidor local de CampusConecta: guarda datos en archivos JSON editables con Bloc de notas."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import json
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'base_de_datos'
DATA.mkdir(exist_ok=True)
DB_FILE = DATA / 'base_de_datos.json'


def load_db():
    try:
        return json.loads(DB_FILE.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError):
        return {}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        if urlparse(self.path).path == '/api/load':
            payload = json.dumps(load_db(), ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(payload)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(payload)
            return
        return super().do_GET()

    def do_POST(self):
        if urlparse(self.path).path != '/api/save':
            self.send_error(404)
            return
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if length > 40 * 1024 * 1024:
                self.send_error(413, 'Datos demasiado grandes')
                return
            body = json.loads(self.rfile.read(length).decode('utf-8'))
            key = str(body.get('key', ''))
            value = body.get('value')
            if not key.startswith('cc_') and key not in ('cc_users', 'cc_posts', 'cc_groups', 'cc_history'):
                self.send_error(400, 'Clave no permitida')
                return
            db = load_db()
            db[key] = value
            serialized = json.dumps(db, ensure_ascii=False, indent=2)
            DB_FILE.write_text(serialized, encoding='utf-8')
            safe_key = ''.join(ch for ch in key if ch.isalnum() or ch in '_-')
            (DATA / f'{safe_key}.json').write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
            response = b'{"ok":true}'
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(response)))
            self.end_headers()
            self.wfile.write(response)
        except Exception as exc:
            self.send_error(400, f'No se pudieron guardar los datos: {exc}')

    def log_message(self, fmt, *args):
        if self.path.startswith('/api/'):
            return
        super().log_message(fmt, *args)


if __name__ == '__main__':
    print('\nCampusConecta está listo en http://127.0.0.1:8000')
    print('Los archivos de texto JSON se guardan en la carpeta base_de_datos.')
    print('Deja esta ventana abierta mientras usas la página. Para detener, presiona Ctrl+C.\n')
    ThreadingHTTPServer(('127.0.0.1', 8000), Handler).serve_forever()
