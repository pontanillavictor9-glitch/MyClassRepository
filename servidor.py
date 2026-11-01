"""
Servidor web: enseña la web del Escaparate y gestiona altas y bajas.

  GET  /                 la web (datos/web/)
  POST /alta             alta gratis → manda un email para CONFIRMAR (doble opt-in:
                         así queda prueba de que la persona lo pidió)
  GET  /confirmar?t=…    activa la suscripción
  GET  /baja?t=…         baja de un clic (y POST /baja para el botón de Gmail/Outlook)

Uso:
    python servidor.py            # http://localhost:8080
Variables: PORT, ENVIO_REAL=1 (si no, los emails de confirmación se guardan en
datos/buzon_salida/ en vez de mandarse).
"""

import os
import time
import urllib.parse
from datetime import datetime
from html import escape
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

import cartero
import comun

ENVIO_REAL = os.environ.get("ENVIO_REAL") == "1"
_ULTIMAS_ALTAS = {}   # ip -> [tiempos], para frenar abusos


def _mensaje(titulo, texto):
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(titulo)}</title>
<link rel="stylesheet" href="/estilo.css"></head><body><div class="wrap" style="padding:40px 16px">
<div class="card"><h1 style="margin-top:0">{escape(titulo)}</h1><p>{texto}</p>
<a class="btn" href="/">Volver</a></div></div></body></html>""".encode("utf-8")


class Manejador(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=str(comun.WEB), **k)

    def _responder(self, codigo, cuerpo):
        self.send_response(codigo)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def _token(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        return (q.get("t") or [""])[0]

    def do_GET(self):
        ruta = urllib.parse.urlparse(self.path).path
        if ruta == "/confirmar":
            return self._confirmar(self._token())
        if ruta == "/baja":
            return self._baja(self._token())
        return super().do_GET()

    def do_POST(self):
        ruta = urllib.parse.urlparse(self.path).path
        largo = min(int(self.headers.get("Content-Length") or 0), 10_000)
        datos = urllib.parse.parse_qs(self.rfile.read(largo).decode("utf-8", "replace"))
        campo = lambda k: (datos.get(k) or [""])[0].strip()
        if ruta == "/alta":
            return self._alta(campo)
        if ruta == "/baja":
            return self._baja(self._token())
        self._responder(404, _mensaje("No encontrado", ""))

    # ------------------------------------------------------------------
    def _alta(self, campo):
        ip = self.client_address[0]
        ahora = time.time()
        recientes = [t for t in _ULTIMAS_ALTAS.get(ip, []) if ahora - t < 3600]
        if len(recientes) >= 5 or campo("web"):          # demasiadas o un robot (campo trampa)
            return self._responder(429, _mensaje("Demasiados intentos", "Prueba más tarde."))
        _ULTIMAS_ALTAS[ip] = recientes + [ahora]

        email = campo("email").lower()
        if "@" not in email or len(email) > 120 or campo("acepto") != "1":
            return self._responder(400, _mensaje("Falta algo", "Revisa el email y marca la casilla de aceptación."))
        sector = campo("sector")
        if sector not in comun.SECTORES:
            return self._responder(400, _mensaje("Falta algo", "Elige a qué te dedicas."))

        clientes = comun.cargar_clientes()
        cli = next((c for c in clientes if c["email"] == email), None)
        if cli is None:
            cli = {"id": f"c{len(clientes) + 1:05d}", "email": email, "plan": "gratis", "enviados": []}
            clientes.append(cli)
        if cli.get("estado") == "activo":
            return self._responder(200, _mensaje("Ya estabas apuntado", "Seguirás recibiendo los avisos."))
        cli.update({
            "nombre": campo("nombre")[:80],
            "sectores": [sector],
            "palabras": [p.strip() for p in campo("palabras").split(",") if p.strip()][:10],
            "provincias": [campo("provincia")] if campo("provincia") else [],
            "estado": "pendiente",
            "token": comun.nuevo_token(),
            "alta_solicitada": datetime.now().isoformat(timespec="seconds"),
            "alta_ip": ip,
        })
        comun.guardar_clientes(clientes)

        enlace = f"{comun.URL_WEB}/confirmar?t={cli['token']}"
        cartero.enviar_email(
            email, f"Confirma tu suscripción a {comun.NOMBRE_SERVICIO}",
            f"Hola,\n\nPara empezar a recibir licitaciones, confirma tu email aquí:\n{enlace}\n\n"
            f"Si no te has apuntado tú, ignora este mensaje y no te escribiremos más.\n\n--\n{comun.TITULAR}",
            de_verdad=ENVIO_REAL)
        self._responder(200, _mensaje("Revisa tu email",
                                      "Te hemos mandado un enlace para confirmar. Si no lo ves, mira en spam."))

    def _confirmar(self, token):
        clientes = comun.cargar_clientes()
        cli = next((c for c in clientes if token and c.get("token") == token), None)
        if not cli or cli.get("estado") == "baja":
            return self._responder(404, _mensaje("Enlace no válido", "Vuelve a apuntarte desde la web."))
        cli["estado"] = "activo"
        cli["confirmado"] = datetime.now().isoformat(timespec="seconds")
        comun.guardar_clientes(clientes)
        self._responder(200, _mensaje("¡Listo!", "El próximo lunes recibirás tus primeras licitaciones."))

    def _baja(self, token):
        clientes = comun.cargar_clientes()
        cli = next((c for c in clientes if token and c.get("token") == token), None)
        if cli:
            # Se borran las preferencias; se guarda solo email + fecha de baja para no
            # volver a escribirle nunca (y poder demostrarlo).
            for k in ("nombre", "sectores", "palabras", "provincias", "enviados", "alta_ip"):
                cli.pop(k, None)
            cli["estado"] = "baja"
            cli["baja"] = datetime.now().isoformat(timespec="seconds")
            comun.guardar_clientes(clientes)
        self._responder(200, _mensaje("Te has dado de baja", "No volverás a recibir emails nuestros."))

    def log_message(self, fmt, *args):
        pass


def main():
    if not (comun.WEB / "index.html").exists():
        import escaparate
        escaparate.generar()
    puerto = int(os.environ.get("PORT", "8080"))
    print(f"Web en http://localhost:{puerto}  (envío real de emails: {'sí' if ENVIO_REAL else 'no'})")
    ThreadingHTTPServer(("", puerto), Manejador).serve_forever()


if __name__ == "__main__":
    main()
