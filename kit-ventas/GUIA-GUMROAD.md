# 🛒 Montar la tienda en Gumroad (20 minutos) y conseguir ventas

Este es el camino "sin vender cara a cara": los productos se venden solos online. Tu única parte imprescindible es crear la cuenta de cobro (tiene que estar a tu nombre, yo no puedo hacerlo) y pegar los enlaces.

## Paso 1 — Crea tu cuenta (5 min)

1. Entra en **gumroad.com** → Sign up (gratis, sin cuota mensual; se quedan ~10% + comisión de pago por cada venta).
2. En Settings → Payments, conecta cómo quieres cobrar (transferencia bancaria o PayPal según país).
   - *Alternativa si Gumroad no paga a tu país: **lemonsqueezy.com** o **payhip.com** — el proceso es casi idéntico.*

## Paso 2 — Sube los 4 productos (15 min)

Los ZIP ya están listos en la carpeta `productos/descargas/` de este repositorio (descárgalos a tu ordenador desde GitHub: entra al archivo → botón "Download raw file").

Para cada producto: **New product → Digital product**, sube el ZIP y usa estos datos:

| Producto | ZIP | Precio |
|---|---|---|
| Plantilla web Barbería/Peluquería con citas por WhatsApp | `plantilla-barberia.zip` | 19 € |
| Plantilla web Restaurante/Bar con reserva de mesa por WhatsApp | `plantilla-restaurante.zip` | 19 € |
| Plantilla web Clínica/Consulta con citas por WhatsApp | `plantilla-clinica.zip` | 19 € |
| Pack 3 plantillas web con reservas por WhatsApp | `pack-completo.zip` | 39 € |

**Descripción para copiar (ajusta el tipo de negocio):**

> Página web profesional para tu [barbería/peluquería] con sistema de citas por WhatsApp integrado: tu cliente elige servicio, día y hora en la web, y la reserva te llega ordenada a tu WhatsApp de siempre.
>
> ✅ Sin saber programar: guía en español paso a paso (15 min)
> ✅ Sin cuotas mensuales: pago único, hosting gratuito
> ✅ Diseño profesional adaptado a móvil
> ✅ Demo real: [enlace a tu demo]
>
> Incluye: plantilla HTML lista para usar + guía de personalización y publicación.

En cada producto, añade el **enlace a la demo en vivo** (tu GitHub Pages) — es lo que más convierte: el comprador puede probar la web antes de pagar.

## Paso 3 — Conecta la tienda a tu web (2 min)

Copia el enlace de venta de cada producto (botón "Share") y pégamelos a mí, o edítalos tú en `index.html`, al final, donde dice:

```
const ENLACES_COMPRA = {
  barberia:    "PEGAR_ENLACE_GUMROAD",
  ...
```

Con eso los botones "Comprar" de tu página quedan activos. **A partir de aquí, cada venta es automática**: pago → descarga → dinero a tu cuenta, sin que tú hagas nada.

## Paso 4 — Que te encuentren (el trabajo real, 30 min/semana)

Ningún producto se vende sin tráfico. Canales gratuitos, de más a menos efectivo:

1. **Gumroad Discover**: se activa solo con las primeras ventas y reseñas — pide reseña a cada comprador.
2. **TikTok / Reels / Shorts** (el más potente sin audiencia previa): vídeos de 20-30 segundos mostrando el móvil: "Así puede ser la web de tu barbería — el cliente pide cita y te llega al WhatsApp". Graba la pantalla de la demo. 2-3 vídeos por semana. No hace falta salir tú ni hablar: pantalla + texto + música.
3. **Grupos de Facebook** de "emprendedores", "peluqueros", "hostelería", "freelancers" de tu país: participa, y cuando alguien pregunte por webs, enseña tu demo. (Aportar primero, vender después — el spam te expulsa.)
4. **Foros y comunidades**: r/emprendedores, IndieHackers, comunidades de Discord de freelancers hispanohablantes.
5. **Tus propias redes**: publica el enlace con la demo. El círculo cercano da las primeras ventas y reseñas.

**A quién le hablas (dos compradores distintos):**
- Dueños de negocio → mensaje: "tu web con citas por WhatsApp por 19 €, sin cuotas".
- **Freelancers/diseñadores** (compran el pack de 39 €): "cobra 200-400 € por web a tus clientes usando estas plantillas — úsalas sin límite".

## Números honestos

- Comisión Gumroad ≈ 10% + pasarela → de 19 € te quedan ~16-17 €.
- Sin promoción: 0-2 ventas/mes. Con 2-3 vídeos semanales constantes: las primeras ventas suelen llegar en 2-4 semanas, y un vídeo que funcione puede disparar el mes.
- El objetivo del primer trimestre es rodar la máquina: 10 ventas/mes ≈ 170 € pasivos. A partir de ahí yo creo más plantillas (tatuadores, gimnasios, talleres, inmobiliarias...) y cada una nueva se apoya en la audiencia ya creada.

## Qué hago yo a partir de aquí

- Crear **más plantillas** para ampliar el catálogo (dímelo y elijo yo los siguientes nichos).
- Versiones **en inglés** para vender al mercado global (mucho más grande).
- **Guiones de los vídeos** de TikTok/Reels: pídemelos y te escribo 10 de golpe, con el texto en pantalla y los pasos de grabación.
- Ajustar precios/textos según lo que veas que funciona.
