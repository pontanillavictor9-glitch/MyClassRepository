# CLAUDE.md

Tienda de recursos imprimibles para profesores de primaria de EE. UU., vendidos en
Teachers Pay Teachers (TPT) y Etsy. Los fabrican agentes; el dueño (Victor) no es
técnico: explícale todo en español, paso a paso, y nunca le pidas contraseñas en el chat.

## Cómo funciona

- `catalogo.py` — la lista de productos. Cada uno: tipo, generador HTML, páginas de muestra, ficha de venta.
- `productos/*.py` — generadores por tipo (multiplicación por código; lectura y descodificables desde `contenido/*.json`).
- `revisor.py` — comprueba el PDF FINAL. Si un producto suspende, NO se publica. No relajes un control para que apruebe: arregla el producto.
- `disenador.py` — portada 2000×2000, muestras con marca de agua, vista previa.
- `tienda.py` — coordina: `python tienda.py [id]` → `salida/<id>/`.
- `investigador.py`, `creador.py` — ideas y contenido nuevo con IA (`ANTHROPIC_API_KEY`).

## Reglas de calidad (no negociables)

1. Las soluciones de matemáticas se calculan por código, nunca las escribe la IA.
2. Todo dato histórico o científico tiene que ser seguro; si hay duda, fuera.
3. Los textos se miden (Flesch-Kincaid) contra el curso; los descodificables, palabra a palabra.
4. Contenido original: nada copiado de otros vendedores, ni personajes o marcas registradas.
5. Tamaño Letter (EE. UU.), fuentes incrustadas, pie de licencia en cada página.

## Publicar (cuando estén las cuentas)

Con Claude en Chrome, en el navegador de Victor, con su sesión ya iniciada. Ritmo de persona:
pocos productos al día por tienda. Nunca crear cuentas, verificar identidad ni tocar datos
bancarios o fiscales: eso lo hace Victor.

## Estado

Ver README.md (tabla de agentes) para lo hecho y lo pendiente.
