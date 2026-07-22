# 🚀 EMPIEZA AQUÍ — Tu negocio de webs para comercios locales

Este repositorio contiene un **negocio completo y listo para arrancar**: vender páginas web con reservas por WhatsApp a negocios locales (peluquerías, bares, restaurantes, clínicas, talleres...).

**El reparto de trabajo es este:**
- **Yo (Claude)** construyo todas las webs: las demos, tu página de venta, y cada web que vendas a un cliente.
- **Tú** enseñas las demos, cierras la venta, cobras, y me pides que personalice la web del cliente.

No necesitas saber programar. Nada.

---

## ✅ Paso 1 — Publica tu página de venta (10 minutos, gratis)

Tu escaparate ya está construido en este repositorio. Para ponerlo online gratis con GitHub Pages:

1. Entra en tu repositorio en GitHub: `github.com/pontanillavictor9-glitch/MyClassRepository`
2. Primero fusiona esta rama con `main` (o pídemelo a mí y te abro un Pull Request).
3. Ve a **Settings → Pages**.
4. En "Source" elige **Deploy from a branch**, rama `main`, carpeta `/ (root)` y pulsa **Save**.
5. En 1-2 minutos tu web estará en: `https://pontanillavictor9-glitch.github.io/MyClassRepository/`

Esa dirección es la que enseñarás a los negocios. Las demos estarán en:
- `.../MyClassRepository/demos/barberia/`
- `.../MyClassRepository/demos/restaurante/`
- `.../MyClassRepository/demos/clinica/`

> 💡 Más adelante, si el negocio funciona, puedes comprar un dominio bonito (ej: `tuweblocal.com`, unos 10 €/año) y conectarlo. Pídemelo y te digo cómo.

## ✅ Paso 2 — Pon TU número de WhatsApp (2 minutos)

En el archivo `index.html` hay una línea al final que dice:

```
const MI_NUMERO = "TUNUMERO";
```

Dímelo y lo cambio yo, o edítalo tú directamente desde GitHub (icono del lápiz). El formato es internacional **sin el "+"**:
- España: `34612345678`
- Colombia: `573001234567`
- México: `5215512345678`

Sin este paso, los botones de "pedir presupuesto" de tu página no te llegarán a ti.

## ✅ Paso 3 — Prepara tu WhatsApp Business (15 minutos, gratis)

Descarga **WhatsApp Business** (gratis, de Meta) y configúralo con:
- **Respuesta automática de bienvenida**: contesta al instante cuando un negocio te escriba (te dejo el texto en `kit-ventas/mensajes-whatsapp.md`).
- **Respuestas rápidas**: atajos para enviar precios y demos con dos toques.
- **Catálogo**: añade tus 3 planes (149 €, 249 €, 19 €/mes) como "productos".

Esto es la versión realista del "bot que responde WhatsApps": respuesta automática inmediata + tú rematas. Un bot 100% automático con la API oficial de WhatsApp es posible más adelante, pero cuesta dinero y de momento no lo necesitas.

## ✅ Paso 4 — Sal a vender (aquí empieza el dinero)

Lee `kit-ventas/GUIA-DE-VENTA.md`. Resumen:

1. Haz una lista de 20 negocios de tu zona **que no tengan web** (búscalos en Google Maps: los que no tienen web o tienen una horrible).
2. Visítalos en persona en hora tranquila, o escríbeles por WhatsApp/Instagram con los mensajes de `kit-ventas/mensajes-whatsapp.md`.
3. Enséñales la demo de su sector **desde tu móvil** y diles: "así quedaría la tuya, con tus fotos y tus precios, en 48 horas".
4. Cierra con el plan de 249 €: pide el 50% por adelantado (Bizum/transferencia/efectivo) y el resto al entregar.

**Meta realista del primer mes**: contactar 40-60 negocios → cerrar 2-4 ventas → 500-1.000 €. A partir de ahí, el boca a boca y las cuotas de mantenimiento (19 €/mes) van sumando ingreso recurrente.

## ✅ Paso 5 — Cuando vendas una web, me la pides a mí

Abre una sesión conmigo (Claude Code) en este repositorio y dime, por ejemplo:

> "Vendí una web a la peluquería 'Estilo Ana'. Aquí tienes sus datos: [servicios y precios, horario, dirección, teléfono/WhatsApp, fotos si las hay]. Créala basándote en la demo de barbería."

Yo creo la web del cliente en una carpeta nueva (ej: `clientes/estilo-ana/`), y quedará online automáticamente en tu misma dirección de GitHub Pages. Entregas, cobras el resto, y a por el siguiente.

---

## 📁 Qué hay en este repositorio

| Archivo/Carpeta | Qué es |
|---|---|
| `index.html` | **Tu página de venta** (el escaparate de TuWebLocal) |
| `demos/barberia/` | Demo funcional: barbería con cita previa por WhatsApp |
| `demos/restaurante/` | Demo funcional: restaurante con reserva de mesa |
| `demos/clinica/` | Demo funcional: clínica dental con solicitud de cita |
| `kit-ventas/GUIA-DE-VENTA.md` | Cómo vender: a quién, qué decir, cómo cobrar, objeciones |
| `kit-ventas/mensajes-whatsapp.md` | Mensajes listos para copiar/pegar y respuestas automáticas |
| `kit-ventas/precios-y-numeros.md` | Tus precios, márgenes y objetivos de ingresos |

## ⚠️ Honestidad por delante

- **Esto no es dinero automático.** Yo hago la parte técnica entera, pero la venta la haces tú: sin enseñar las demos a negocios, no hay ingresos.
- **Yo no puedo escribir a los negocios por ti** ni cobrar por ti — no tengo acceso a tu WhatsApp ni a cuentas de pago, y el contacto tiene que ser tuyo y personal (el spam masivo mata el negocio antes de empezar).
- **Lo bueno**: cada web te cuesta 0 € producirla (la hago yo, el hosting es gratis), así que casi todo lo que cobres es margen.

**Tu único trabajo esta semana**: pasos 1-3 (30 minutos) y visitar tus primeros 10 negocios.
