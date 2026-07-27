# 🛒 Cómo replicar esta página en tu tienda Shopify

La landing de `tienda/index.html` sigue el formato clásico de tienda monoproducto
(estilo Koriderm). Esta guía te dice cómo montar **cada sección en Shopify**,
usando el tema gratuito **Dawn** (el que viene por defecto) y sin apps de pago.

> Abre `ver-tienda.bat` para tener la landing de referencia delante mientras
> montas tu Shopify: vas copiando sección a sección los textos que ya están
> escritos en `tienda/js/productos.js`.

## Preparación

1. En Shopify: **Tienda online → Temas** → comprueba que usas **Dawn** (gratis).
2. Pulsa **Personalizar** → arriba, cambia de "Página de inicio" a
   **Productos → Ficha de producto predeterminada**. Todo lo siguiente se hace aquí.
3. Las secciones se añaden con **"Agregar sección"** en la columna izquierda.

## Sección a sección

| Sección de la landing | Cómo hacerla en Dawn |
|---|---|
| Barra de oferta (arriba) | En la cabecera: sección **"Barra de anuncios"** → escribe la oferta de lanzamiento |
| Héroe: fotos + título + puntos ✓ | Es la propia ficha de producto: sube 3-6 **fotos reales** del proveedor, pega el título y en la descripción los 3 puntos con ✓ |
| Valoración ★★★★★ | App gratuita **"Judge.me"** (u otra de reseñas): muestra estrellas junto al título. Sin reseñas reales aún, NO pongas número inventado |
| Selector de packs 1/2/3 | En el producto crea una **variante** llamada "Cantidad" con opciones "1 unidad / Pack 2 (ahorra 10 €) / Pack 3 (ahorra 25 €)", cada una con su precio. El precio tachado es el campo **"Precio de comparación"** |
| Sellos ✓ garantía/pago/envío | Sección **"Texto enriquecido"** con iconos, o bloques de **"Multicolumna"** justo bajo el botón |
| Problema → solución | Sección **"Imagen con texto"**: foto del gato + el texto del problema (cópialo de `productos.js`) |
| Beneficios (6 tarjetas) | Sección **"Multicolumna"**: un bloque por beneficio, con el emoji en el título |
| Cómo funciona 1-2-3 | Otra **"Multicolumna"** de 3 columnas |
| Reseñas | La app de reseñas (Judge.me) tiene su propia sección "Reviews". Pide reseña por email a cada cliente real |
| Comparativa cuenco vs fuente | Sección **"Texto enriquecido"** con una tabla, o una imagen comparativa |
| Garantía 30 días | Sección **"Imagen con texto"** o "Texto enriquecido" con fondo de color |
| FAQ desplegable | Sección **"Contenido desplegable"** (collapsible content) — Dawn la trae de serie |
| Barra pegajosa de compra | Dawn ya la incluye: en la ficha de producto, activa **"Botón de pago dinámico/pegajoso"** si tu versión lo trae |

## Los textos: cópialos, ya están escritos

Todos los textos de venta (título, problema, beneficios, pasos, FAQ, garantía)
están en **`tienda/js/productos.js`** en español y listos para pegar.
Solo cambia lo que no encaje con TU anuncio del proveedor.

## Checklist antes de publicar

- [ ] Fotos reales del proveedor subidas (pide las originales o haz las tuyas al recibir tu pedido de prueba)
- [ ] Variantes de pack con **precio** y **precio de comparación** puestos
- [ ] Página de **Aviso legal, Privacidad y Devoluciones** (Shopify las genera: Configuración → Políticas)
- [ ] **Pagos** activados (Shopify Payments / PayPal)
- [ ] Envío gratis configurado (Configuración → Envío)
- [ ] Producto vinculado en **DSers** a la variante correcta (almacén España/Europa)
- [ ] Pedido de prueba hecho por ti

## ⚠️ Reglas de honestidad (te ahorran problemas legales)

- Nada de reseñas inventadas ni contadores de "4,8/5 con 2.000 clientes" si no es verdad.
- Nada de temporizadores falsos de "la oferta acaba en 10:00 minutos" que se reinician.
- El descuento tachado debe ser creíble (no "antes 199 €").
- Promete solo lo que el anuncio del proveedor realmente dice del producto.
