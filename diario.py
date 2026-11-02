"""
El día, en orden: Atención (primero, para no escribir a quien pidió la baja) →
Buscador (si se le pasan búsquedas) → Redactor → Cartero.

    python diario.py                                    # sin mandar (para revisar)
    python diario.py --enviar                           # mandando de verdad
    python diario.py --buscar "dentist|Austin, TX" --buscar "auto repair|Tampa, FL"
"""

import argparse
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).parent


def paso(nombre, *args):
    print(f"\n=== {nombre} ===", flush=True)
    return subprocess.run([sys.executable, str(RAIZ / f"{nombre}.py"), *args]).returncode


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--enviar", action="store_true")
    a.add_argument("--buscar", action="append", default=[], help='"tipo|ciudad"')
    x = a.parse_args()
    errores = paso("atencion", *(["--enviar"] if x.enviar else []))
    for b in x.buscar:
        tipo, ciudad = b.split("|", 1)
        errores += paso("buscador", "--tipo", tipo.strip(), "--ciudad", ciudad.strip())
    errores += paso("redactor")
    errores += paso("cartero", *(["--enviar"] if x.enviar else []))
    sys.exit(1 if errores else 0)


if __name__ == "__main__":
    main()
