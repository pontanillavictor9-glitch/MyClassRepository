"""
Agente 1 — RECOLECTOR

Baja las licitaciones nuevas de la Plataforma de Contratación del Sector
Público (datos abiertos, formato ATOM + CODICE) y las guarda limpias en
datos/licitaciones/AAAA-MM-DD.jsonl, una licitación por línea.

Uso:
    python recolector.py                 # últimos 2 días desde la web oficial
    python recolector.py --dias 7        # última semana
    python recolector.py --fichero x.atom   # leer un fichero ya bajado (pruebas)

Solo usa la biblioteca estándar de Python: no hay que instalar nada.
"""

import argparse
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Feed oficial de licitaciones (perfiles del contratante, todas las administraciones
# que publican en la Plataforma). Va de lo más nuevo a lo más viejo y se pagina con
# <link rel="next">.
FEED_URL = ("https://contrataciondelsectorpublico.gob.es/sindicacion/"
            "sindicacion_643/licitacionesPerfilesContratanteCompleto3.atom")

import comun
CARPETA_DATOS = comun.LICITACIONES

TIPOS = {"1": "Suministros", "2": "Servicios", "3": "Obras"}

ESTADOS = {
    "PRE": "Anuncio previo",
    "PUB": "En plazo",
    "EV": "Pendiente de adjudicación",
    "ADJ": "Adjudicada",
    "RES": "Resuelta",
    "ANUL": "Anulada",
}


# ---------------------------------------------------------------------------
# Lectura del XML sin depender de los prefijos de namespace (la Plataforma
# cambia de versión de CODICE y los namespaces bailan).
# ---------------------------------------------------------------------------

def _local(tag):
    return tag.rsplit("}", 1)[-1]


def _hijo(el, nombre):
    if el is None:
        return None
    for h in el:
        if _local(h.tag) == nombre:
            return h
    return None


def _ruta(el, *nombres):
    for n in nombres:
        el = _hijo(el, n)
    return el


def _texto(el, *nombres):
    el = _ruta(el, *nombres)
    return el.text.strip() if el is not None and el.text else None


def _todos(el, nombre):
    """Todos los descendientes con ese nombre local."""
    if el is None:
        return []
    return [x for x in el.iter() if _local(x.tag) == nombre]


def _numero(t):
    try:
        return float(t) if t is not None else None
    except ValueError:
        return None


def parsear_entrada(entry):
    """Convierte un <entry> del feed en un diccionario limpio."""
    cfs = None
    for x in entry.iter():
        if _local(x.tag) == "ContractFolderStatus":
            cfs = x
            break

    enlace = None
    for l in entry:
        if _local(l.tag) == "link" and l.get("href"):
            enlace = l.get("href")
            break

    lic = {
        "id": _texto(entry, "id"),
        "actualizado": _texto(entry, "updated"),
        "titulo": _texto(entry, "title"),
        "enlace": enlace,
    }
    if cfs is None:
        return lic

    proyecto = _hijo(cfs, "ProcurementProject")
    proceso = _hijo(cfs, "TenderingProcess")
    tipo = _texto(proyecto, "TypeCode")
    estado = _texto(cfs, "ContractFolderStatusCode")

    fin = _texto(proceso, "TenderSubmissionDeadlinePeriod", "EndDate")
    hora = _texto(proceso, "TenderSubmissionDeadlinePeriod", "EndTime")

    documentos = []
    for nombre in ("LegalDocumentReference", "TechnicalDocumentReference",
                   "AdditionalDocumentReference"):
        for d in _todos(cfs, nombre):
            uri = None
            for u in _todos(d, "URI"):
                if u.text:
                    uri = u.text.strip()
                    break
            if uri:
                documentos.append({"tipo": nombre.replace("DocumentReference", ""),
                                   "nombre": _texto(d, "ID"), "url": uri})

    lic.update({
        "expediente": _texto(cfs, "ContractFolderID"),
        "estado_codigo": estado,
        "estado": ESTADOS.get(estado, estado),
        "organo": _texto(cfs, "LocatedContractingParty", "Party", "PartyName", "Name"),
        "objeto": _texto(proyecto, "Name"),
        "tipo_codigo": tipo,
        "tipo": TIPOS.get(tipo, f"Otro ({tipo})" if tipo else None),
        "importe_sin_iva": _numero(_texto(proyecto, "BudgetAmount", "TaxExclusiveAmount")),
        "valor_estimado": _numero(_texto(proyecto, "BudgetAmount",
                                         "EstimatedOverallContractAmount")),
        "cpv": [c.text.strip() for c in _todos(proyecto, "ItemClassificationCode") if c.text],
        "provincia": _texto(proyecto, "RealizedLocation", "CountrySubentity"),
        "nuts": _texto(proyecto, "RealizedLocation", "CountrySubentityCode"),
        "fin_plazo": f"{fin}T{hora}" if fin and hora else fin,
        "procedimiento_codigo": _texto(proceso, "ProcedureCode"),
        "documentos": documentos,
    })
    return lic


def parsear_pagina(xml_bytes):
    """Devuelve (licitaciones, url_siguiente_pagina)."""
    raiz = ET.fromstring(xml_bytes)
    siguiente = None
    entradas = []
    for el in raiz:
        n = _local(el.tag)
        if n == "link" and el.get("rel") == "next":
            siguiente = el.get("href")
        elif n == "entry":
            entradas.append(parsear_entrada(el))
    return entradas, siguiente


# ---------------------------------------------------------------------------
# Descarga
# ---------------------------------------------------------------------------

def bajar(url):
    req = urllib.request.Request(url, headers={"User-Agent": "alertas-licitaciones/0.1"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def _fecha(t):
    if not t:
        return None
    try:
        return datetime.fromisoformat(t.replace("Z", "+00:00"))
    except ValueError:
        return None


def recolectar_web(dias, max_paginas=200):
    limite = datetime.now(timezone.utc) - timedelta(days=dias)
    url, todas = FEED_URL, []
    for pagina in range(1, max_paginas + 1):
        print(f"  página {pagina}…", file=sys.stderr)
        entradas, url = parsear_pagina(bajar(url))
        todas.extend(entradas)
        fechas = [f for f in (_fecha(e.get("actualizado")) for e in entradas) if f]
        if not url or (fechas and min(fechas) < limite):
            break
    return [e for e in todas if (_fecha(e.get("actualizado")) or limite) >= limite]


# ---------------------------------------------------------------------------
# Guardado y resumen
# ---------------------------------------------------------------------------

def guardar(licitaciones):
    """Guarda sin duplicar: si un expediente ya está en el fichero del día, se
    sustituye por la versión más reciente."""
    CARPETA_DATOS.mkdir(parents=True, exist_ok=True)
    fichero = CARPETA_DATOS / f"{datetime.now():%Y-%m-%d}.jsonl"
    previas = {}
    if fichero.exists():
        for linea in fichero.read_text(encoding="utf-8").splitlines():
            if linea.strip():
                e = json.loads(linea)
                previas[e["id"]] = e
    for e in licitaciones:
        if e.get("id"):
            previas[e["id"]] = e
    with fichero.open("w", encoding="utf-8") as f:
        for e in previas.values():
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    return fichero, len(previas)


def resumen(licitaciones):
    abiertas = [e for e in licitaciones if e.get("estado_codigo") == "PUB"]
    print(f"\nLicitaciones leídas: {len(licitaciones)}")
    print(f"En plazo (se puede presentar oferta): {len(abiertas)}")
    total = sum(e.get("importe_sin_iva") or 0 for e in abiertas)
    print(f"Dinero en juego en las abiertas (sin IVA): {total:,.0f} €".replace(",", "."))

    for titulo, clave in (("Por tipo", "tipo"), ("Por provincia", "provincia")):
        print(f"\n{titulo}:")
        for k, n in Counter(e.get(clave) or "¿?" for e in abiertas).most_common(10):
            print(f"  {n:5}  {k}")

    # Las dos primeras cifras del CPV dicen el sector (45 = obras, 90 = limpieza…).
    print("\nPor sector (CPV, 2 primeras cifras):")
    sectores = Counter(c[:2] for e in abiertas for c in set(x[:2] for x in e.get("cpv", [])))
    for k, n in sectores.most_common(10):
        print(f"  {n:5}  {k}")


def main():
    p = argparse.ArgumentParser(description="Baja las licitaciones públicas nuevas.")
    p.add_argument("--dias", type=int, default=2, help="cuántos días atrás (por defecto 2)")
    p.add_argument("--fichero", help="leer un .atom local en vez de la web")
    p.add_argument("--no-guardar", action="store_true", help="solo enseñar el resumen")
    a = p.parse_args()

    if a.fichero:
        lics, _ = parsear_pagina(Path(a.fichero).read_bytes())
    else:
        lics = recolectar_web(a.dias)

    if not a.no_guardar:
        fichero, n = guardar(lics)
        print(f"Guardadas {n} licitaciones en {fichero}")
    resumen(lics)


if __name__ == "__main__":
    main()
