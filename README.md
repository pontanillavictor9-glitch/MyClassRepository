# Alertas de licitaciones

Servicio de suscripción: cada mañana, cada cliente recibe por email los contratos
públicos que le encajan (por sector y provincia), resumidos por IA en un minuto
de lectura. Totalmente automático; el dueño solo contesta emails.

El motor está pensado para servir después también **alertas de subvenciones**
(mismo esquema: bajar datos públicos → resumir → emparejar → enviar).

## Los agentes

| # | Agente | Estado |
|---|---|---|
| 1 | **Recolector**: baja las licitaciones nuevas de la Plataforma de Contratación | ✅ primera versión |
| 2 | Analista: lee los pliegos (PDF) y saca importe, plazo y requisitos | pendiente |
| 3 | Emparejador: decide qué licitaciones le encajan a cada cliente | pendiente |
| 4 | Cartero: manda el email diario a cada suscriptor | pendiente |
| 5 | Escaparate: páginas públicas por sector y provincia para Google | pendiente |
| 6 | Atención: lee los emails recibidos y avisa solo de lo importante | pendiente |

## Probar el Recolector

Necesita Python 3 y nada más.

```
python recolector.py --dias 2
```

Baja los dos últimos días de la Plataforma de Contratación del Sector Público
(datos abiertos oficiales), guarda cada licitación en
`datos/licitaciones/AAAA-MM-DD.jsonl` y enseña un resumen: cuántas hay en plazo,
cuánto dinero suman, por tipo, provincia y sector.

Sin internet, con el ejemplo escrito a mano (no son datos reales):

```
python recolector.py --fichero muestra/ejemplo.atom --no-guardar
```

## Reglas del negocio

- Solo se manda email a quien se ha suscrito. Nada de emails en frío (LSSI art. 21).
- Captación: páginas para Google + versión gratis semanal + prueba pequeña de anuncios.
