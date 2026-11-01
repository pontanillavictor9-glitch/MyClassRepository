"""
Agente 3 — EMPAREJADOR

Decide qué licitaciones abiertas le encajan a cada cliente activo, según:
  - sectores: prefijos CPV ("90" = limpieza, "9091" = limpieza de edificios…)
  - palabras: palabras clave que busca en el objeto del contrato
  - provincias: dónde trabaja (vacío = toda España)
  - importe_min / importe_max: tamaño de contrato que puede asumir

Nunca repite una licitación que ya se le mandó. Deja la lista de cada cliente en
datos/envios/AAAA-MM-DD/<cliente>.json para que el Cartero la envíe.

Uso:
    python emparejador.py
"""

import json

import comun

PLAN_GRATIS_MAX = 3      # el plan gratis recibe solo las 3 mejores, una vez por semana
PLAN_PAGO_MAX = 40


def puntuar(lic, cli):
    """0 = no encaja. Cuanto más alto, mejor encaja."""
    # Zona: se manda si el contrato es de una de sus provincias, de la comunidad
    # que la contiene o de toda España. Un contrato de otra zona no se manda.
    codigos = [c for p in cli.get("provincias", []) for c in comun.nuts_de_provincia(p)]
    nuts = lic.get("nuts") or ""
    amb = comun.ambito(lic)
    if codigos:
        if amb == "provincia" and nuts not in codigos:
            return 0
        if amb == "region" and not any(c.startswith(nuts) for c in codigos):
            return 0
        if nuts == "ESZZZ":        # «extra-regio»: se ejecuta fuera de España
            return 0

    importe = lic.get("importe_sin_iva")
    if importe is not None:
        if cli.get("importe_min") and importe < cli["importe_min"]:
            return 0
        if cli.get("importe_max") and importe > cli["importe_max"]:
            return 0

    puntos = 0
    cpvs = lic.get("cpv", [])
    for pref in cli.get("sectores", []):
        if any(c.startswith(pref) for c in cpvs):
            puntos = max(puntos, 2 + len(pref))   # prefijo más largo = más preciso

    texto = comun.normalizar(f"{lic.get('objeto')} {lic.get('titulo')}")
    for palabra in cli.get("palabras", []):
        if comun.normalizar(palabra) in texto:
            puntos += 3

    if puntos and codigos and amb != "provincia":
        puntos -= 1        # contrato regional, nacional o sin zona: se manda, pero más abajo
    return max(puntos, 0)


def toca_enviar(cli, fecha):
    """El plan gratis solo recibe los lunes."""
    from datetime import date
    if cli.get("plan") == "pago":
        return True
    return date.fromisoformat(fecha).weekday() == 0


def emparejar(fecha=None, forzar=False):
    fecha = fecha or comun.hoy()
    lics = comun.abiertas(comun.licitaciones_recientes())
    carpeta = comun.ENVIOS / fecha
    carpeta.mkdir(parents=True, exist_ok=True)
    resumen = []
    for cli in comun.cargar_clientes():
        if cli.get("estado") != "activo" or not (forzar or toca_enviar(cli, fecha)):
            continue
        ya = set(cli.get("enviados", []))
        candidatas = [(puntuar(l, cli), l) for l in lics if l["id"] not in ya]
        candidatas = sorted([c for c in candidatas if c[0] > 0],
                            key=lambda c: (-c[0], -(c[1].get("importe_sin_iva") or 0)))
        maximo = PLAN_PAGO_MAX if cli.get("plan") == "pago" else PLAN_GRATIS_MAX
        elegidas = [l for _, l in candidatas[:maximo]]
        (carpeta / f"{cli['id']}.json").write_text(json.dumps({
            "cliente": cli["id"], "fecha": fecha, "total_encajan": len(candidatas),
            "licitaciones": elegidas}, ensure_ascii=False, indent=1), encoding="utf-8")
        resumen.append((cli["id"], len(elegidas), len(candidatas)))
    return resumen


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--forzar", action="store_true", help="preparar también al plan gratis aunque no sea lunes")
    a = p.parse_args()
    for cid, n, total in emparejar(forzar=a.forzar):
        print(f"  {cid}: {n} licitaciones (encajan {total})")


if __name__ == "__main__":
    main()
