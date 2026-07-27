// Feed de precios en tiempo real desde el WebSocket público de Binance.
// No requiere API key. Se suscribe a los símbolos favoritos + los de posiciones abiertas.

import WebSocket from 'ws';

const BINANCE_WS = 'wss://stream.binance.com:9443/ws';

export class PriceFeed {
  constructor(symbols = []) {
    this.symbols = new Set(symbols.map(s => s.toUpperCase()));
    this.ws = null;
    this.listeners = new Set();
    this.reconnectDelay = 1000;
    this.subId = 1;
  }

  onPrice(fn) {
    this.listeners.add(fn);
  }

  addSymbol(symbol) {
    symbol = symbol.toUpperCase();
    if (this.symbols.has(symbol)) return;
    this.symbols.add(symbol);
    this._subscribe([symbol]);
  }

  start() {
    this._connect();
  }

  _connect() {
    try {
      this.ws = new WebSocket(BINANCE_WS);
    } catch (err) {
      console.error('[precios] Error creando WebSocket:', err.message);
      this._scheduleReconnect();
      return;
    }

    this.ws.on('open', () => {
      console.log('[precios] Conectado a Binance');
      this.reconnectDelay = 1000;
      this._subscribe([...this.symbols]);
    });

    this.ws.on('message', raw => {
      try {
        const msg = JSON.parse(raw.toString());
        // miniTicker: { e: '24hrMiniTicker', s: 'BTCUSDT', c: 'ultimo precio', ... }
        if (msg.e === '24hrMiniTicker' && msg.s && msg.c) {
          const price = parseFloat(msg.c);
          for (const fn of this.listeners) fn(msg.s, price);
        }
      } catch { /* mensaje no JSON, ignorar */ }
    });

    this.ws.on('close', () => {
      console.warn('[precios] Conexión con Binance cerrada, reconectando...');
      this._scheduleReconnect();
    });

    this.ws.on('error', err => {
      console.error('[precios] Error de WebSocket:', err.message);
      try { this.ws.close(); } catch { /* ya cerrado */ }
    });
  }

  _scheduleReconnect() {
    setTimeout(() => this._connect(), this.reconnectDelay);
    this.reconnectDelay = Math.min(this.reconnectDelay * 2, 30000);
  }

  _subscribe(symbols) {
    if (!symbols.length || !this.ws || this.ws.readyState !== WebSocket.OPEN) return;
    const params = symbols.map(s => `${s.toLowerCase()}@miniTicker`);
    this.ws.send(JSON.stringify({ method: 'SUBSCRIBE', params, id: this.subId++ }));
  }
}
