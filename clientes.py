"""
Gestión de clientes a mano, para el dueño.

    python clientes.py listar
    python clientes.py pago correo@empresa.es     # cuando te paga: pasa al plan completo
    python clientes.py gratis correo@empresa.es   # si deja de pagar
    python clientes.py baja correo@empresa.es     # si te pide la baja por otra vía
"""

import sys
from collections import Counter

import comun


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    orden = sys.argv[1]
    clientes = comun.cargar_clientes()
    if orden == "listar":
        for c in clientes:
            print(f"  {c['id']}  {c.get('estado', '?'):9} {c.get('plan', '?'):6} {c['email']}  "
                  f"{','.join(comun.SECTORES.get(s[:2], s) for s in c.get('sectores', []))}")
        cuenta = Counter((c.get("estado"), c.get("plan")) for c in clientes)
        print(f"\nActivos de pago: {cuenta[('activo', 'pago')]} · activos gratis: {cuenta[('activo', 'gratis')]}"
              f" · pendientes de confirmar: {sum(v for (e, _), v in cuenta.items() if e == 'pendiente')}")
        return
    if len(sys.argv) < 3 or orden not in ("pago", "gratis", "baja"):
        print(__doc__)
        return
    email = sys.argv[2].lower()
    c = next((c for c in clientes if c["email"] == email), None)
    if not c:
        print(f"No encuentro a {email}")
        return
    if orden == "baja":
        for k in ("nombre", "sectores", "palabras", "provincias", "enviados", "alta_ip"):
            c.pop(k, None)
        c["estado"] = "baja"
        c["baja"] = comun.hoy()
    else:
        c["plan"] = orden
    comun.guardar_clientes(clientes)
    print(f"{email}: {c.get('estado')} / {c.get('plan')}")


if __name__ == "__main__":
    main()
