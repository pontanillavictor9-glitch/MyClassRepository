# Tienda de recursos para profesores (TPT + Etsy)

Agentes que fabrican fichas imprimibles para profesores de primaria de EE. UU.
y las dejan listas para subir a **Teachers Pay Teachers** y **Etsy**.

## Fabricar

```
python tienda.py                 # todos los productos del catálogo
python tienda.py multiplicacion-g3
```

Cada producto aprobado queda en `salida/<producto>/`:

| Fichero | Para qué |
|---|---|
| `producto.pdf` | Lo que descarga el comprador |
| `portada.png` | Primera imagen del anuncio (2000×2000) |
| `muestra-N.png` | Imágenes de muestra con marca de agua |
| `vista_previa.pdf` | El «Preview» que pide TPT |
| `ficha.json` | Título, precio, cursos, estándares |
| `revision.txt` | Informe del Revisor |

## Los agentes

| Agente | Fichero | Estado |
|---|---|---|
| Investigador | `investigador.py` | Hecho (necesita clave de IA) |
| Creador | `productos/*.py`, `creador.py` | Hecho. Matemáticas sin IA; textos con IA o a mano |
| Revisor | `revisor.py` | Hecho. Comprueba el PDF final; con clave de IA, además ortografía y datos |
| Diseñador | `disenador.py` | Hecho |
| Escaparate, Publicador, Atención, Analista | — | Siguiente fase |

## Primeros 3 productos

| Producto | Páginas | Precio sugerido | Cómo se garantiza la calidad |
|---|---|---|---|
| Multiplication Fact Fluency Drills, Grade 3 | 22 | 4,00 $ | Las 470 soluciones se releen del PDF y se recalculan |
| Thanksgiving Reading Comprehension, Grade 3 | 12 | 3,50 $ | Nivel de lectura medido (2.8–4.3), datos históricos contrastados |
| Silent e Decodable Passages, Grade 1 | 13 | 3,00 $ | Cada palabra comprobada con las reglas de descodificación |

## Requisitos

Python 3 con `pypdf` y `Pillow`, y Playwright (`pip install playwright` y
`python -m playwright install chromium`). La IA es opcional: `ANTHROPIC_API_KEY`.
El nombre de la tienda se pone en la variable `MARCA` (por defecto «Sunny Desk Studio»).

Fuentes: Fredoka y Lexend (Google Fonts, licencia OFL: uso comercial permitido).
