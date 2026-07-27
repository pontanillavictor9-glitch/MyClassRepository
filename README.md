# 📈 Trading Live Studio

Plataforma todo-en-uno para hacer **trading en directo** en YouTube, Twitch y TikTok:

- 💬 **Chat unificado**: los chats de Twitch, YouTube Live y TikTok Live en un solo panel (y como overlay para el stream).
- 📊 **Panel de operaciones en vivo**: cuenta simulada (paper trading) con precios reales de Binance en tiempo real. Abre y cierra posiciones long/short y ve el P&L al segundo.
- 💰 **Overlay de beneficio del día**: beneficio realizado + flotante, siempre visible en el stream.
- ⚠️ **Overlay de aviso legal rotativo**: el típico "esto no es una recomendación de inversión, es solo entretenimiento".
- 🌐 **Página de comunidad**: landing con tus enlaces (Discord, Telegram, redes) para que la gente se una.

Todo funciona **sin API keys**: la lectura de chats usa conexiones públicas y los precios vienen del WebSocket público de Binance.

---

## 🚀 Puesta en marcha

Necesitas [Node.js](https://nodejs.org) 18 o superior.

```bash
# 1. Instalar dependencias
npm install

# 2. Crear tu configuración
cp config.example.json config.json
#    → edita config.json con tus canales y tu nombre

# 3. Arrancar
npm start
```

Al arrancar verás las URLs en la consola:

| Página | URL | Para qué |
|---|---|---|
| Panel de control | `http://localhost:3000/panel.html` | TU pantalla privada: abrir/cerrar operaciones y ver el multichat |
| Comunidad | `http://localhost:3000/` | Landing pública con tus enlaces |
| Overlay posiciones | `http://localhost:3000/overlay/positions` | Fuente de navegador en OBS |
| Overlay beneficio del día | `http://localhost:3000/overlay/daily` | Fuente de navegador en OBS |
| Overlay disclaimer | `http://localhost:3000/overlay/disclaimer` | Fuente de navegador en OBS |
| Overlay chat unificado | `http://localhost:3000/overlay/chat` | Fuente de navegador en OBS |

## ⚙️ Configuración (`config.json`)

```jsonc
{
  "puerto": 3000,
  "nombreComunidad": "Mi Comunidad de Trading",
  "panelToken": "cambia-esto",        // clave para poder operar desde el panel
  "cuenta": {
    "balanceInicial": 10000,          // balance de la cuenta simulada
    "moneda": "USD"
  },
  "simbolosFavoritos": ["BTCUSDT", "ETHUSDT"],  // pares de Binance
  "chats": {
    "twitch":  { "activo": true, "canal": "tu_canal" },
    "youtube": { "activo": true, "canal": "@TuCanal" },   // handle, channelId (UC...) o id del vídeo en directo
    "tiktok":  { "activo": true, "usuario": "tu_usuario" }
  },
  "disclaimers": [ "frases que rotan en el overlay..." ],
  "comunidad": { "enlaces": { "discord": "https://...", "telegram": "https://..." } }
}
```

Notas sobre los chats:

- **Twitch**: lectura anónima por IRC. Solo el nombre del canal, sin credenciales.
- **YouTube**: funciona cuando hay un **directo activo** en el canal. Acepta handle (`@MiCanal`), channelId (`UC...`) o el id del vídeo en directo. Si no hay directo, reintenta cada 30 s automáticamente.
- **TikTok**: funciona cuando estás **en directo** en TikTok. Igual: reintenta solo hasta que empieces.

## 🎥 Configurar OBS

1. En OBS, añade una **Fuente → Navegador** por cada overlay.
2. URL: la del overlay (p. ej. `http://localhost:3000/overlay/positions`).
3. Tamaños recomendados: posiciones `700×300`, beneficio del día `320×140`, disclaimer `900×80`, chat `400×600`.
4. Los overlays tienen **fondo transparente**: colócalos encima de tu escena de gráficos.
5. **Importante**: nunca captures la ventana del panel de control (`/panel.html`) — es tu pantalla privada y contiene el token.

El overlay del disclaimer **déjalo visible durante todo el directo**: además de protegerte, las políticas de monetización de YouTube/Twitch/TikTok ven con buenos ojos los avisos claros en contenido financiero.

## 🧪 Cómo funciona la cuenta simulada

- Los precios son **reales**, del WebSocket público de Binance (pares spot como `BTCUSDT`).
- Al abrir una operación se registra el precio actual como entrada; el P&L flotante se recalcula con cada tick.
- Al cerrar, el P&L se consolida en el balance y en el **beneficio del día** (realizado + flotante), que es lo que muestra el overlay.
- El estado se guarda en `data/state.json`, así que sobrevive a reinicios.
- Botón de emergencia: `POST /api/reset` (con el token) restaura el balance inicial.

## 🔒 Seguridad

- Pon un `panelToken` fuerte en `config.json`: cualquier acción que modifique operaciones lo exige.
- El servidor está pensado para ejecutarse **en tu propio PC** (localhost) junto a OBS. Si lo expones a internet, ponlo detrás de HTTPS y no compartas la URL del panel.

## ⚠️ Aviso legal — léelo en serio

Esta plataforma incluye los overlays de disclaimer porque **son necesarios**, pero un banner no lo cubre todo:

- Emitir tu operativa como **entretenimiento/educación** con avisos claros es generalmente seguro.
- **Vender señales de trading es otra cosa**: en España y en la UE, las recomendaciones de inversión están reguladas (MiFID II, Reglamento de Abuso de Mercado, criterios de la **CNMV** sobre señales y "finfluencers"). Cobrar por señales concretas de compra/venta puede considerarse un servicio de inversión que requiere autorización, y hacerlo sin ella conlleva sanciones.
- Antes de monetizar señales, **consulta con un abogado especializado en regulación financiera**. Alternativas de monetización con menos riesgo regulatorio: suscripciones de canal, membresías con contenido educativo, comunidad de Discord/Telegram centrada en formación y análisis general (no señales personalizadas de "compra ahora").

Nada en este repositorio constituye asesoramiento financiero ni legal.
