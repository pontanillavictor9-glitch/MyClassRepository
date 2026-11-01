"""
Piezas compartidas por todos los agentes: rutas, lectura de datos, sectores,
clientes y configuración (todo por variables de entorno, nunca contraseñas en
el código).
"""

import json
import os
import secrets
import unicodedata
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).parent
# Se puede mover todo a otra carpeta (por ejemplo un disco del servidor) con DATOS_DIR.
DATOS = Path(os.environ.get("DATOS_DIR", RAIZ / "datos"))

LICITACIONES = DATOS / "licitaciones"
ANALISIS = DATOS / "analisis"
ENVIOS = DATOS / "envios"
BUZON_SALIDA = DATOS / "buzon_salida"
AVISOS = DATOS / "avisos"
WEB = DATOS / "web"
CLIENTES = DATOS / "clientes.json"

NOMBRE_SERVICIO = os.environ.get("NOMBRE_SERVICIO", "Alertas de Licitaciones")
URL_WEB = os.environ.get("URL_WEB", "http://localhost:8080").rstrip("/")
EMAIL_REMITENTE = os.environ.get("EMAIL_REMITENTE", "avisos@ejemplo.invalid")
# Datos legales del remitente: la LSSI obliga a identificarse en cada email.
TITULAR = os.environ.get("TITULAR", "[TU NOMBRE O EMPRESA] · [NIF] · [DIRECCIÓN]")
ENLACE_PAGO = os.environ.get("ENLACE_PAGO", "")  # p. ej. un Payment Link de Stripe


# Divisiones CPV (dos primeras cifras): el sector del contrato.
SECTORES = {
    "03": "Agricultura, ganadería y pesca", "09": "Combustibles y energía",
    "14": "Minería", "15": "Alimentación y bebidas", "18": "Ropa y calzado",
    "22": "Imprenta y publicaciones", "24": "Productos químicos",
    "30": "Equipos de oficina e informática", "31": "Material eléctrico",
    "32": "Telecomunicaciones (equipos)", "33": "Material sanitario",
    "34": "Vehículos y transporte", "35": "Seguridad y defensa",
    "37": "Deporte y música (material)", "38": "Laboratorio y precisión",
    "39": "Mobiliario y equipamiento", "41": "Agua", "42": "Maquinaria industrial",
    "43": "Maquinaria de obra", "44": "Materiales de construcción",
    "45": "Obras de construcción", "48": "Software", "50": "Reparación y mantenimiento",
    "51": "Instalación de equipos", "55": "Hostelería y catering", "60": "Transporte",
    "63": "Servicios auxiliares de transporte y viajes", "64": "Correos y telecomunicaciones",
    "65": "Suministros públicos", "66": "Banca y seguros", "70": "Inmobiliarios",
    "71": "Arquitectura e ingeniería", "72": "Servicios informáticos", "73": "I+D",
    "75": "Administración pública", "76": "Servicios petroleros y de gas",
    "77": "Jardinería y servicios forestales", "79": "Servicios a empresas (legal, consultoría, marketing)",
    "80": "Educación y formación", "85": "Salud y servicios sociales",
    "90": "Limpieza, residuos y medio ambiente", "92": "Ocio, cultura y deporte",
    "98": "Otros servicios",
}


def normalizar(t):
    """minúsculas y sin tildes, para comparar provincias y palabras."""
    t = unicodedata.normalize("NFKD", t or "")
    return "".join(c for c in t if not unicodedata.combining(c)).lower().strip()


def slug(t):
    return "-".join("".join(c if c.isalnum() else " " for c in normalizar(t)).split())


def hoy():
    return f"{datetime.now():%Y-%m-%d}"


def leer_jsonl(fichero):
    if not Path(fichero).exists():
        return []
    return [json.loads(l) for l in Path(fichero).read_text(encoding="utf-8").splitlines() if l.strip()]


def licitaciones_recientes(dias=7):
    """Todas las licitaciones guardadas en los últimos ficheros diarios, sin
    duplicados (gana la versión más reciente)."""
    ficheros = sorted(LICITACIONES.glob("*.jsonl"))[-dias:]
    por_id = {}
    for f in ficheros:
        for e in leer_jsonl(f):
            por_id[e["id"]] = e
    return list(por_id.values())


def abiertas(licitaciones, ahora=None):
    ahora = ahora or datetime.now()
    salida = []
    for e in licitaciones:
        if e.get("estado_codigo") != "PUB":
            continue
        fin = e.get("fin_plazo")
        if fin:
            try:
                if datetime.fromisoformat(fin) < ahora:
                    continue
            except ValueError:
                pass
        salida.append(e)
    return salida


def analisis_de(lic):
    f = ANALISIS / f"{clave(lic)}.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else None


def clave(lic):
    import hashlib
    return hashlib.sha1((lic.get("id") or "").encode()).hexdigest()[:16]


# --------------------------------------------------------------------------
# Clientes (datos personales: el fichero real NO va a git, ver .gitignore)
# --------------------------------------------------------------------------

def cargar_clientes():
    if not CLIENTES.exists():
        return []
    return json.loads(CLIENTES.read_text(encoding="utf-8"))


def guardar_clientes(clientes):
    CLIENTES.parent.mkdir(parents=True, exist_ok=True)
    tmp = CLIENTES.with_suffix(".tmp")
    tmp.write_text(json.dumps(clientes, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(CLIENTES)


def nuevo_token():
    return secrets.token_urlsafe(24)


def euros(x):
    if x is None:
        return "importe no indicado"
    return f"{x:,.0f} €".replace(",", ".")
