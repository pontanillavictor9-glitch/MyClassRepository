"""
Piezas compartidas: configuración (todo por variables de entorno, nunca claves
en el código), rutas, lectura/escritura de prospectos y la lista de supresión
(quien pide no recibir más emails no vuelve a recibir NINGUNO, nunca).
"""

import json
import os
import re
import unicodedata
import urllib.request
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).parent
DATOS = Path(os.environ.get("DATOS_DIR", RAIZ / "datos"))
PROSPECTOS = DATOS / "prospectos.json"
SUPRESION = DATOS / "supresion.txt"
BUZON_SALIDA = DATOS / "buzon_salida"
AVISOS = DATOS / "avisos"
REGISTRO = DATOS / "registro_envios.jsonl"

# --- quién manda los emails (la ley de EE. UU., CAN-SPAM, obliga a decirlo) ---
MARCA = os.environ.get("MARCA", "ReplyDesk")
REMITENTE_NOMBRE = os.environ.get("REMITENTE_NOMBRE", "Victor")
EMAIL_REMITENTE = os.environ.get("EMAIL_REMITENTE", "hello@ejemplo.invalid")
DIRECCION_POSTAL = os.environ.get("DIRECCION_POSTAL", "[DIRECCIÓN POSTAL REAL OBLIGATORIA]")
PRECIO = os.environ.get("PRECIO", "$49/month")
ENLACE_PAGO = os.environ.get("ENLACE_PAGO", "")

MODELO_IA = os.environ.get("MODELO_IA", "claude-opus-5-5")
AGENTE_HTTP = "Mozilla/5.0 (compatible; ReplyDeskBot/0.1)"


def ahora():
    return datetime.now().isoformat(timespec="seconds")


def hoy():
    return f"{datetime.now():%Y-%m-%d}"


def normalizar(t):
    t = unicodedata.normalize("NFKD", t or "")
    return "".join(c for c in t if not unicodedata.combining(c)).lower().strip()


def slug(t):
    return "-".join("".join(c if c.isalnum() else " " for c in normalizar(t)).split())


# --------------------------------------------------------------------------
# HTTP (una sola función, así las pruebas la pueden sustituir sin internet)
# --------------------------------------------------------------------------

def http(url, datos=None, cabeceras=None, timeout=30, maximo=3_000_000):
    """GET (o POST si hay datos JSON). Devuelve bytes."""
    cuerpo = json.dumps(datos).encode() if datos is not None else None
    cab = {"User-Agent": AGENTE_HTTP, **(cabeceras or {})}
    if cuerpo is not None:
        cab.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=cuerpo, headers=cab)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(maximo)


def http_json(url, datos=None, cabeceras=None, timeout=30):
    return json.loads(http(url, datos, cabeceras, timeout))


# --------------------------------------------------------------------------
# Prospectos: un diccionario por negocio, guardado en datos/prospectos.json
#   estado: nuevo → listo (tiene borrador) → enviado → seguimiento → respondio
#           | descartado | baja
# --------------------------------------------------------------------------

def cargar_prospectos():
    if not PROSPECTOS.exists():
        return {}
    return json.loads(PROSPECTOS.read_text(encoding="utf-8"))


def guardar_prospectos(p):
    PROSPECTOS.parent.mkdir(parents=True, exist_ok=True)
    tmp = PROSPECTOS.with_suffix(".tmp")
    tmp.write_text(json.dumps(p, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(PROSPECTOS)


# --------------------------------------------------------------------------
# Lista de supresión: emails y dominios que no se tocan nunca más
# --------------------------------------------------------------------------

def suprimidos():
    if not SUPRESION.exists():
        return set()
    return {l.strip().lower() for l in SUPRESION.read_text(encoding="utf-8").splitlines() if l.strip()}


def suprimir(email):
    email = (email or "").strip().lower()
    if not email or email in suprimidos():
        return
    SUPRESION.parent.mkdir(parents=True, exist_ok=True)
    with SUPRESION.open("a", encoding="utf-8") as f:
        f.write(email + "\n")


def esta_suprimido(email):
    email = (email or "").lower()
    s = suprimidos()
    return email in s or ("@" + email.split("@")[-1]) in s


EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
