// Trading Live Studio — servidor principal.
// Une el motor de paper trading, el feed de precios de Binance, los chats de
// Twitch/YouTube/TikTok y sirve el panel de control + overlays para OBS.

import fs from 'fs';
import http from 'http';
import path from 'path';
import express from 'express';
import { WebSocketServer, WebSocket } from 'ws';
import { TradingEngine } from './src/tradingEngine.js';
import { PriceFeed } from './src/priceFeed.js';
import { startTwitchChat } from './src/chat/twitch.js';
import { startYouTubeChat } from './src/chat/youtube.js';
import { startTikTokChat } from './src/chat/tiktok.js';

// ---------- Configuración ----------
const CONFIG_FILE = fs.existsSync('config.json') ? 'config.json' : 'config.example.json';
const config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
if (CONFIG_FILE === 'config.example.json') {
  console.warn('⚠️  No existe config.json — usando config.example.json. Copia el ejemplo y personalízalo:');
  console.warn('    cp config.example.json config.json');
}

const PORT = process.env.PORT || config.puerto || 3000;
const PANEL_TOKEN = process.env.PANEL_TOKEN || config.panelToken || '';

// ---------- Motor de trading + precios ----------
const engine = new TradingEngine(config.cuenta || {});
const feed = new PriceFeed([
  ...(config.simbolosFavoritos || []),
  ...engine.symbolsInUse()
]);

feed.onPrice((symbol, price) => {
  engine.updatePrice(symbol, price);
});
feed.start();

// ---------- Servidor HTTP + WebSocket ----------
const app = express();
app.use(express.json());
app.use(express.static('public'));

const server = http.createServer(app);
const wss = new WebSocketServer({ server, path: '/ws' });

const chatBuffer = []; // últimas 100 líneas para clientes que se conectan tarde

function broadcast(msg) {
  const raw = JSON.stringify(msg);
  for (const client of wss.clients) {
    if (client.readyState === WebSocket.OPEN) client.send(raw);
  }
}

wss.on('connection', ws => {
  ws.send(JSON.stringify({ type: 'state', data: engine.snapshot() }));
  ws.send(JSON.stringify({ type: 'config', data: publicConfig() }));
  for (const m of chatBuffer.slice(-50)) {
    ws.send(JSON.stringify({ type: 'chat', data: m }));
  }
});

// Estado a todos los clientes: al cambiar (abrir/cerrar) y cada segundo con precios frescos
engine.onChange(() => broadcast({ type: 'state', data: engine.snapshot() }));
setInterval(() => broadcast({ type: 'state', data: engine.snapshot() }), 1000);

function onChatMessage(msg) {
  chatBuffer.push(msg);
  if (chatBuffer.length > 100) chatBuffer.shift();
  broadcast({ type: 'chat', data: msg });
}

// ---------- Conectar chats ----------
const chats = config.chats || {};
if (chats.twitch?.activo && chats.twitch.canal) {
  startTwitchChat(chats.twitch.canal, onChatMessage);
}
if (chats.youtube?.activo && chats.youtube.canal) {
  startYouTubeChat(chats.youtube.canal, onChatMessage);
}
if (chats.tiktok?.activo && chats.tiktok.usuario) {
  startTikTokChat(chats.tiktok.usuario, onChatMessage);
}

// ---------- API ----------
function publicConfig() {
  return {
    nombreComunidad: config.nombreComunidad,
    streamer: config.streamer,
    disclaimers: config.disclaimers || [],
    comunidad: config.comunidad || {},
    simbolosFavoritos: config.simbolosFavoritos || [],
    moneda: config.cuenta?.moneda || 'USD'
  };
}

app.get('/api/config', (req, res) => res.json(publicConfig()));
app.get('/api/state', (req, res) => res.json(engine.snapshot()));

// Las rutas que MODIFICAN el estado requieren el token del panel (si está configurado)
function requireToken(req, res, next) {
  if (PANEL_TOKEN && req.headers['x-panel-token'] !== PANEL_TOKEN) {
    return res.status(401).json({ error: 'Token del panel incorrecto' });
  }
  next();
}

app.post('/api/trade/open', requireToken, (req, res) => {
  try {
    const { symbol, side, qty } = req.body || {};
    feed.addSymbol(String(symbol || '').toUpperCase());
    const pos = engine.open({ symbol, side, qty });
    res.json(pos);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

app.post('/api/trade/close', requireToken, (req, res) => {
  try {
    res.json(engine.close(req.body?.id));
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

app.post('/api/reset', requireToken, (req, res) => {
  engine.reset();
  res.json({ ok: true });
});

// Rutas cómodas para los overlays
app.get('/overlay/:name', (req, res, next) => {
  const file = path.resolve('public', 'overlay', `${req.params.name}.html`);
  if (fs.existsSync(file)) return res.sendFile(file);
  next();
});

server.listen(PORT, () => {
  console.log('');
  console.log('🚀 Trading Live Studio en marcha');
  console.log(`   Panel de control:      http://localhost:${PORT}/panel.html`);
  console.log(`   Página de comunidad:   http://localhost:${PORT}/`);
  console.log('   Overlays para OBS (fuente de navegador):');
  console.log(`     Posiciones en vivo:  http://localhost:${PORT}/overlay/positions`);
  console.log(`     Beneficio del día:   http://localhost:${PORT}/overlay/daily`);
  console.log(`     Disclaimer legal:    http://localhost:${PORT}/overlay/disclaimer`);
  console.log(`     Chat unificado:      http://localhost:${PORT}/overlay/chat`);
  console.log('');
});
