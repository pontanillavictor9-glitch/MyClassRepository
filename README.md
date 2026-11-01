# Alertas de licitaciones

Servicio de suscripción: cada mañana, cada cliente recibe por email los contratos
públicos que le encajan (por sector y provincia), resumidos por IA en un minuto
de lectura. Funciona solo; el dueño solo contesta los emails que el agente
Atención le marca.

El motor está pensado para servir después también **alertas de subvenciones**
(mismo esquema: bajar datos públicos → resumir → emparejar → enviar).

## Los agentes

| # | Fichero | Qué hace |
|---|---|---|
| 1 | `recolector.py` | Baja las licitaciones nuevas de la Plataforma de Contratación del Sector Público (datos abiertos). |
| 2 | `analista.py` | Lee los pliegos (PDF) con IA y saca resumen, requisitos, criterios y dificultad. Sin clave de IA, hace un resumen básico. |
| 3 | `emparejador.py` | Elige para cada cliente las que le encajan (sector CPV, palabras, provincia, importe). Nunca repite. |
| 4 | `cartero.py` | Monta el email de cada cliente. Por defecto **no manda nada**: lo deja en `datos/buzon_salida/` para revisarlo. |
| 5 | `escaparate.py` | Genera la web: portada con alta gratis y precios + una página por sector y por sector+provincia (para Google) + sitemap. |
| 6 | `atencion.py` | Lee el buzón: da de baja sola a quien lo pide, y del resto te manda un aviso con un borrador de respuesta. Nunca contesta por su cuenta. |

Además:

- `servidor.py` — sirve la web y gestiona altas (con email de confirmación), confirmaciones y bajas de un clic.
- `clientes.py` — para ti: `listar`, `pago <email>` (cuando alguien paga), `gratis`, `baja`.
- `diario.py` — corre los seis agentes en orden. Es lo que se programa para cada mañana.

## Probarlo (sin internet ni cuentas)

```
python diario.py --prueba
```

Usa `muestra/ejemplo.atom` (escrito a mano, **no son datos reales**). Para tener
clientes de prueba, copia `clientes.ejemplo.json` a `datos/clientes.json` antes.

## Planes

- **Gratis:** 3 licitaciones cada lunes. Es el gancho.
- **Completo (29 €/mes):** todas las que encajan, cada mañana, con requisitos, criterios y dificultad.

## Lo que falta para ponerlo en marcha (no es código)

1. **Comprobar los datos reales:** el Recolector aún no se ha probado contra la web oficial (desde la sesión donde se escribió estaba bloqueada).
2. **Un servidor** donde corra `servidor.py` y `diario.py` cada mañana.
3. **Un dominio** y un **proveedor de email** (SMTP para mandar, IMAP para leer).
4. **Clave de IA** (`ANTHROPIC_API_KEY`) para los resúmenes buenos. El modelo se elige con `MODELO_IA`.
5. **Alta de autónomo** para poder cobrar, y un **enlace de pago** (`ENLACE_PAGO`, por ejemplo un Payment Link de Stripe).
6. **Rellenar** `TITULAR` (nombre, NIF, dirección) y revisar las plantillas de privacidad y aviso legal.

## Variables de entorno

| Variable | Para qué |
|---|---|
| `DATOS_DIR` | Carpeta de datos (por defecto `datos/`) |
| `URL_WEB`, `NOMBRE_SERVICIO`, `TITULAR` | Datos públicos del servicio |
| `EMAIL_REMITENTE`, `SMTP_HOST`, `SMTP_PORT`, `SMTP_USUARIO`, `SMTP_CLAVE` | Envío de emails |
| `IMAP_HOST`, `IMAP_USUARIO`, `IMAP_CLAVE`, `EMAIL_AVISOS` | Lectura del buzón y a dónde te llegan los avisos |
| `ANTHROPIC_API_KEY`, `MODELO_IA` | IA (opcional) |
| `ENLACE_PAGO` | Botón de pago del plan completo |
| `ENVIO_REAL=1` | Que el servidor mande de verdad los emails de confirmación |
| `PORT` | Puerto del servidor (8080) |

## Reglas del negocio (legales)

- Solo se escribe a quien se ha suscrito **y ha confirmado su email** (doble opt-in). Nada de emails en frío (LSSI art. 21).
- Cada email lleva quién lo manda y un enlace de baja de un clic.
- Al darse de baja se borran las preferencias; solo queda el email y la fecha, para no volver a escribirle.
- `datos/clientes.json` tiene datos personales: **nunca** se sube a git (está en `.gitignore`).
