# Respuestas a reseñas de Google para negocios de EE. UU.

Servicio hecho por nosotros: contestamos las reseñas de Google de negocios locales
de EE. UU. (dentistas, talleres, clínicas, restaurantes…) por una cuota mensual.
El dueño no configura nada.

**Cómo se consiguen clientes:** el email de presentación ya lleva las respuestas
escritas a sus últimas reseñas, listas para pegar. Ve el trabajo hecho antes de pagar.

## Fase 1: comprobar que se vende (lo que hay construido)

| # | Fichero | Qué hace |
|---|---|---|
| 1 | `buscador.py` | Busca negocios en Google Maps por tipo y ciudad; se queda con los que tienen ≥20 reseñas, web, email de contacto y (si se sabe) ≥2 reseñas recientes sin contestar. |
| 2 | `redactor.py` | Con IA escribe en inglés las respuestas a sus 3 últimas reseñas, el email de presentación y un seguimiento. |
| 3 | `cartero.py` | Manda el email y, si no contesta en 4 días, UN seguimiento. Máximo 30 al día, espaciados. Por defecto **no manda nada**: los deja en `datos/buzon_salida/` para revisarlos. |
| 4 | `atencion.py` | Lee las respuestas: bajas → lista de supresión para siempre; automáticas → se ignoran; el resto → te avisa **en español**, con un borrador de respuesta en inglés y su traducción. |

- `diario.py` — lo corre todo en orden (Atención va primero).
- `prueba.py` — prueba completa sin internet, con negocios inventados: `python prueba.py`

**Objetivo de la prueba:** 200-300 emails. Si responden interesados 5 o más, se construye
la fase 2 (el agente que contesta las reseñas de los clientes cada día).

## Lo que necesitas (en orden)

1. **Clave de Google Places** (`GOOGLE_PLACES_KEY`): Google Cloud, activar "Places API (New)".
   Pedir las reseñas cuesta más que una búsqueda normal; mira el precio antes.
2. **Clave de SerpApi** (`SERPAPI_KEY`, de pago, opcional pero muy recomendable): Google Places
   **no dice si el dueño ha respondido** una reseña. Sin SerpApi el email no puede decir
   "tienes X sin responder" y se escribirá a negocios que ya contestan.
3. **Clave de IA** (`ANTHROPIC_API_KEY`). El modelo se elige con `MODELO_IA`.
4. **Un dominio aparte solo para esto** (no el principal) y un buzón con SMTP/IMAP. Hay que
   configurar SPF, DKIM y DMARC y "calentar" el buzón 2-3 semanas antes de mandar en serio,
   o los emails acabarán en spam.
5. **Dirección postal real** (`DIRECCION_POSTAL`): la ley de EE. UU. la exige en cada email.
   El cartero se niega a mandar sin ella.
6. **Enlace de pago** (`ENLACE_PAGO`, p. ej. Stripe) y alta de autónomo.

## Variables de entorno

| Variable | Para qué |
|---|---|
| `GOOGLE_PLACES_KEY`, `SERPAPI_KEY` | Búsqueda de negocios y reseñas |
| `ANTHROPIC_API_KEY`, `MODELO_IA` | IA |
| `MARCA`, `REMITENTE_NOMBRE`, `EMAIL_REMITENTE`, `DIRECCION_POSTAL`, `PRECIO`, `ENLACE_PAGO` | Quién eres y qué ofreces |
| `SMTP_HOST`, `SMTP_PORT`, `SMTP_USUARIO`, `SMTP_CLAVE` | Mandar |
| `IMAP_HOST`, `IMAP_USUARIO`, `IMAP_CLAVE`, `EMAIL_AVISOS` | Leer respuestas y avisarte |
| `LIMITE_DIARIO` (30), `DIAS_SEGUIMIENTO` (4), `MIN_RESENAS` (20), `MIN_SIN_RESPONDER` (2) | Ajustes |
| `DATOS_DIR` | Carpeta de datos |

## Reglas legales que el código ya cumple

- **CAN-SPAM (EE. UU.):** remitente y asunto veraces, dirección postal, baja clara y respetada
  para siempre (`datos/supresion.txt`), cabecera `List-Unsubscribe`.
- **RGPD (tú estás en la UE):** solo emails públicos de contacto del negocio sacados de su web,
  un primer email y un único seguimiento, y supresión inmediata. Base: interés legítimo.
  **Confírmalo con un gestor o abogado antes de empezar.**
- La IA nunca contesta sola a nadie: tú decides.

## Lo que no se ha podido probar aún

Desde la sesión donde se escribió solo se alcanzaba Google; SerpApi y las webs de los
negocios estaban bloqueadas, y no había claves. Todo está probado con `prueba.py`
(respuestas simuladas), pero **falta la primera prueba con datos reales**.
