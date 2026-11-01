"""
El día entero, en orden: Recolector → Analista → Emparejador → Cartero →
Escaparate → Atención. Es lo que hay que programar para que corra solo cada
mañana (por ejemplo a las 7:00).

Uso:
    python diario.py               # todo, pero SIN mandar emails (los deja para revisar)
    python diario.py --enviar      # todo, mandando de verdad
    python diario.py --prueba      # con el ejemplo de muestra/, sin internet
"""

import argparse
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).parent


def paso(nombre, *args):
    print(f"\n=== {nombre} ===", flush=True)
    r = subprocess.run([sys.executable, str(RAIZ / f"{nombre}.py"), *args])
    if r.returncode:
        print(f"  ¡{nombre} terminó con error {r.returncode}! Sigo con el resto.", flush=True)
    return r.returncode


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--enviar", action="store_true")
    p.add_argument("--prueba", action="store_true")
    a = p.parse_args()
    errores = 0
    if a.prueba:
        errores += paso("recolector", "--fichero", str(RAIZ / "muestra" / "ejemplo.atom"))
    else:
        errores += paso("recolector", "--dias", "2")
    errores += paso("analista")
    errores += paso("emparejador", *(["--forzar"] if a.prueba else []))
    errores += paso("cartero", *(["--enviar"] if a.enviar else []))
    errores += paso("escaparate")
    errores += paso("atencion", *(["--enviar"] if a.enviar else []))
    sys.exit(1 if errores else 0)


if __name__ == "__main__":
    main()
