# 🛍️ Tienda de Dropshipping — plantilla + guía

Esta carpeta contiene una **tienda online de demostración** totalmente funcional
(catálogo, fichas de producto, carrito) y esta guía con los pasos reales para
lanzar un negocio de dropshipping.

## Cómo ver la tienda

**Windows (fácil):** doble clic en `ver-tienda.bat` (en la raíz del repositorio).

**Cualquier sistema:**

```bash
npm install        # solo la primera vez
npm run tienda     # abre http://localhost:4000
```

## Cómo personalizarla

| Quiero cambiar… | Archivo |
|---|---|
| Los productos, precios y textos | `tienda/js/productos.js` |
| El nombre y eslogan de la tienda | `tienda/js/productos.js` (bloque `TIENDA`) |
| Los colores y el diseño | `tienda/css/estilos.css` (variables de `:root`) |
| Las imágenes | `tienda/img/` (sustituye los SVG por fotos reales del proveedor) |

---

# 📈 El negocio, paso a paso (sin humo)

Antes de nada, la verdad incómoda: el dropshipping **no es dinero fácil**. Es un
negocio real con márgenes ajustados, mucha competencia y donde la mayoría del
trabajo es marketing, no programación. Se puede ganar dinero, pero casi siempre
tras varios intentos fallidos y gastando en publicidad para aprender. Empieza
pequeño y no inviertas dinero que no puedas permitirte perder.

## 1. Elige un nicho (no "una tienda de todo")

Las tiendas generalistas casi nunca funcionan: compites con Amazon. Busca un
nicho concreto donde puedas destacar:

- **Buenas señales:** producto que resuelve un problema, difícil de encontrar en
  tiendas físicas, ligero y barato de enviar, margen ×2.5–×3 posible, público
  apasionado (mascotas, gaming, fitness, bebés, setup de escritorio…).
- **Malas señales:** electrónica frágil o con garantías complicadas, ropa con
  tallas (muchas devoluciones), productos con marca registrada (te pueden
  denunciar), cualquier cosa que toque salud o vaya a la piel/boca.

**Dónde investigar:** TikTok/Instagram (busca "TikTok made me buy it"),
AliExpress "más vendidos", los anuncios que te salen a ti (Facebook Ad Library
es pública), Google Trends para ver si la demanda sube o baja.

## 2. Encuentra proveedores

| Proveedor | Para qué |
|---|---|
| **AliExpress** | Empezar y validar. Envíos lentos (1–3 semanas). |
| **CJ Dropshipping** | Envíos más rápidos, hace de intermediario, se integra con Shopify. |
| **Spocket / BigBuy** | Proveedores con almacén en Europa → envíos en 2–5 días. |
| **Zendrop** | Alternativa popular con branding personalizado. |

Antes de vender un producto: **pídetelo a ti** para comprobar calidad y tiempos
reales. Un producto malo = devoluciones + reseñas negativas + disputas de pago.

## 3. Calcula el margen ANTES de vender

Regla rápida: precio de venta ≈ **3× el coste del proveedor**. En
`js/productos.js` cada producto tiene `costeProveedor` justo para esto:

```
Precio de venta        34,99 €
− Coste proveedor      12,40 €
− Envío                 3,00 €
− Comisión de pago      ~1,30 € (Stripe/PayPal ~3%)
− Publicidad           ~10,00 € (¡el gasto más grande!)
= Beneficio             ~8,30 € por venta
```

Si después de la publicidad no queda margen, el producto no vale, por muy bien
que se venda.

## 4. Crea la tienda

Dos caminos:

- **Shopify (recomendado para vender de verdad):** ~36 €/mes, pagos y envíos
  resueltos, apps como DSers/CJ que pasan los pedidos al proveedor
  automáticamente. Es el estándar del sector porque tu tiempo vale más que la
  cuota.
- **Tienda propia (como esta plantilla):** gratis y controlas todo, pero tienes
  que añadir tú la pasarela de pago (Stripe/PayPal), los emails de pedido, etc.
  Esta carpeta te sirve para **aprender, maquetar y validar diseño/nicho** antes
  de pagar Shopify.

## 5. Imágenes y contenido

- Usa las fotos y vídeos del proveedor **solo como base**; los que ganan dinero
  graban sus propios vídeos (o encargan uno en Fiverr/Billo) porque el vídeo es
  lo que vende en TikTok/Meta.
- Reescribe las descripciones: beneficio primero ("adiós dolor de cuello"),
  característica después ("aluminio plegable").
- Los SVG de `img/` son marcadores de posición: sustitúyelos por fotos reales
  (mismo nombre de archivo y no tocas nada más).

## 6. Tráfico: aquí se gana o se pierde

Sin visitas no hay ventas, y las visitas se pagan:

- **TikTok orgánico:** gratis, publica 1–3 vídeos/día del producto. Lento pero
  sin riesgo. Ideal para empezar.
- **Meta Ads / TikTok Ads:** rápido pero caro. Presupuesto mínimo realista para
  probar un producto: 100–150 € (y darlo por perdido si no funciona).
- **Influencers micro:** enviarles el producto gratis a cambio de vídeo.

Mide siempre: si con 30–50 € de anuncios sobre un producto no hay NINGUNA
venta ni carritos, cambia de creatividad o de producto. No "esperes a que
arranque".

## 7. Lo legal (importante, no lo saltes)

- Para facturar necesitas darte de **alta como autónomo** (España) o el
  equivalente de tu país, y declarar IVA. Infórmate antes de la primera venta.
- Obligatorio en la web: aviso legal, política de privacidad (RGPD), política
  de devoluciones (en la UE el cliente tiene **14 días** por ley) y condiciones
  de compra.
- Nada de marcas registradas (logos de Disney, equipos de fútbol…): denuncia y
  cierre de cuenta garantizados.
- El IVA de importación y aduanas existen: con proveedor europeo (Spocket,
  BigBuy) te ahorras casi todos esos líos.

## 8. Plan de acción para tus primeras 2 semanas

1. **Días 1–2:** elige nicho y 3–5 productos candidatos (usa los criterios del punto 1).
2. **Días 3–4:** pide muestras del mejor candidato. Mientras llegan…
3. **Días 5–7:** monta la tienda: edita `js/productos.js`, colores en `estilos.css`, textos de venta.
4. **Días 8–10:** graba 5–10 vídeos cortos del producto para TikTok.
5. **Días 11–14:** publica a diario, mide qué vídeo engancha, y solo entonces decide si pasas a Shopify + anuncios de pago.

---

⚠️ **Recuerda:** el botón "Finalizar compra" de esta demo no cobra de verdad.
Es una plantilla de aprendizaje y validación, no una pasarela de pagos.
