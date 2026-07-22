# 💈 Plantilla web para Barbería / Peluquería — con citas por WhatsApp

¡Gracias por tu compra! En 15-20 minutos tendrás tu web funcionando, **sin saber programar**.

## Qué incluye
- `index.html` — la web completa: servicios con precios, horario, mapa y **formulario de cita previa que llega directo a tu WhatsApp**.

## Paso 1 — Pon tus datos (10 min)

Abre `index.html` con cualquier editor de texto (Bloc de notas en Windows, TextEdit en Mac) y cambia:

1. **Tu número de WhatsApp** (lo más importante). Busca esta línea casi al final:
   ```
   const TELEFONO = "34600000000";
   ```
   Pon tu número en formato internacional SIN el "+". Ejemplos: España `34612345678`, México `5215512345678`, Colombia `573001234567`.
2. **El nombre del negocio**: busca "Barbería El Clásico" (aparece varias veces) y reemplázalo por el tuyo (usa Ctrl+H / "buscar y reemplazar").
3. **Servicios y precios**: busca la sección `id="servicios"` y edita los textos y precios.
4. **Horario y dirección**: busca la sección `id="horario"`.
5. **El teléfono visible**: busca "600 00 00 00" y pon el tuyo.

💡 Consejo: guarda y abre el archivo con doble clic en tu navegador para ver los cambios al momento.

## Paso 2 — Publícala gratis (5 min)

La forma más fácil, sin registros complicados:
1. Entra en **app.netlify.com/drop** (crea cuenta gratis si te la pide).
2. Arrastra la carpeta con tu `index.html` a la página.
3. Listo: tendrás una dirección tipo `tunegocio.netlify.app`. Puedes cambiar el nombre en Site settings → Change site name.

Alternativas gratuitas: GitHub Pages, Cloudflare Pages, Vercel.

## Paso 3 — Haz que te encuentren
- Pega el enlace en tu **perfil de Instagram** y en tu **ficha de Google Maps** (Google Business → Editar perfil → Sitio web).
- Haz una reserva de prueba desde otro móvil para comprobar que te llega al WhatsApp.

## Preguntas rápidas
- **¿Cuotas mensuales?** Ninguna. La web es tuya y el hosting recomendado es gratuito.
- **¿Cambiar colores?** Busca `:root{` al principio del archivo: ahí están los colores (`--gold`, `--dark`...). Cambia los códigos por los de tu marca (búscalos en Google: "color picker").
- **¿Un dominio propio (minegocio.com)?** Se compra aparte (~10-15 €/año en Namecheap o similar) y se conecta desde Netlify en 2 clics.

Licencia: uso para tu negocio o para webs de tus clientes. No está permitido revender la plantilla tal cual.
