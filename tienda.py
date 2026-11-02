"""
COORDINADOR. Lleva cada producto del catálogo por la cadena:

    Creador (PDF) → Revisor (si falla, se para) → Diseñador (portada y muestras)

y deja todo listo para subir en salida/<producto>/:
    producto.pdf, vista_previa.pdf, portada.png, muestra-N.png,
    ficha.json (título, precio, cursos…) y revision.txt (el informe del Revisor).

Uso:
    python tienda.py                      # todos los productos
    python tienda.py multiplicacion-g3    # solo uno
"""

import shutil
import sys

import catalogo
import comun
import disenador
import revisor


def fabricar(pid):
    prod = catalogo.PRODUCTOS[pid]
    carpeta = comun.SALIDA / pid
    if carpeta.exists():
        shutil.rmtree(carpeta)
    carpeta.mkdir(parents=True)

    # 1. Creador
    html = prod["html"]()
    pdf = comun.pdf(html, carpeta / "producto.pdf")

    # 2. Revisor
    fallos, avisos = [], []
    textos = revisor.comunes(pdf, fallos, avisos)
    datos = {}
    if prod["tipo"] == "matematicas":
        datos["soluciones_comprobadas"] = revisor.matematicas(textos, prod["problemas"](), fallos)
    elif prod["tipo"] == "lectura":
        datos["nivel_lectura"] = revisor.lectura(textos, comun.leer_json(comun.CONTENIDO / prod["contenido"]), fallos, avisos)
    elif prod["tipo"] == "decodables":
        revisor.decodables(comun.leer_json(comun.CONTENIDO / prod["contenido"]), fallos, avisos)
    revisor.con_ia(textos, fallos, avisos)

    informe = [f"Producto: {pid}", f"Páginas: {len(textos)}", f"Datos: {datos}", "",
               "RESULTADO: " + ("APROBADO" if not fallos else "SUSPENDIDO"), ""]
    informe += [f"FALLO: {f}" for f in fallos] + [f"aviso: {a}" for a in avisos]
    (carpeta / "revision.txt").write_text("\n".join(informe) + "\n", encoding="utf-8")
    if fallos:
        return False, len(textos), fallos, avisos

    # 3. Diseñador
    _, tmp = disenador.muestras(html, prod["muestras"], carpeta)
    paginas = [tmp / f"p{i + 1}.png" for i in prod["muestras"][:3]]
    disenador.portada(prod["ficha"], [paginas[2], paginas[1], paginas[0]], carpeta, prod["colores"])
    shutil.rmtree(tmp)

    comun.escribir_json(carpeta / "ficha.json", {**prod["ficha"], "id": pid, "paginas": len(textos)})
    return True, len(textos), fallos, avisos


def main():
    ids = sys.argv[1:] or list(catalogo.PRODUCTOS)
    for pid in ids:
        ok, n, fallos, avisos = fabricar(pid)
        print(f"{'APROBADO ' if ok else 'SUSPENDIDO'}  {pid}  ({n} páginas)")
        for f in fallos:
            print(f"    FALLO: {f}")
        for a in avisos:
            print(f"    aviso: {a}")


if __name__ == "__main__":
    main()
