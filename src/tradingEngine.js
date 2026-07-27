// Motor de paper trading: gestiona posiciones, P&L y beneficio diario.
// El estado se persiste en data/state.json para sobrevivir reinicios.

import fs from 'fs';
import path from 'path';

const DATA_DIR = path.resolve('data');
const STATE_FILE = path.join(DATA_DIR, 'state.json');

function hoy() {
  return new Date().toISOString().slice(0, 10);
}

export class TradingEngine {
  constructor({ balanceInicial = 10000, moneda = 'USD' } = {}) {
    this.moneda = moneda;
    this.prices = new Map(); // symbol -> último precio
    this.listeners = new Set();
    this.state = {
      balanceInicial,
      balance: balanceInicial,
      positions: [],
      history: [],
      realizadoPorDia: {},
      nextId: 1
    };
    this._load(balanceInicial);
  }

  _load(balanceInicial) {
    try {
      if (fs.existsSync(STATE_FILE)) {
        const saved = JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
        this.state = { ...this.state, ...saved };
      } else {
        this.state.balanceInicial = balanceInicial;
        this.state.balance = balanceInicial;
      }
    } catch (err) {
      console.error('[engine] No se pudo cargar el estado guardado:', err.message);
    }
  }

  _save() {
    try {
      fs.mkdirSync(DATA_DIR, { recursive: true });
      fs.writeFileSync(STATE_FILE, JSON.stringify(this.state, null, 2));
    } catch (err) {
      console.error('[engine] No se pudo guardar el estado:', err.message);
    }
  }

  onChange(fn) {
    this.listeners.add(fn);
  }

  _emit() {
    for (const fn of this.listeners) fn(this.snapshot());
  }

  updatePrice(symbol, price) {
    this.prices.set(symbol, price);
  }

  symbolsInUse() {
    return [...new Set(this.state.positions.map(p => p.symbol))];
  }

  open({ symbol, side, qty }) {
    symbol = String(symbol || '').toUpperCase().trim();
    qty = Number(qty);
    if (!symbol) throw new Error('Falta el símbolo');
    if (side !== 'long' && side !== 'short') throw new Error('side debe ser "long" o "short"');
    if (!Number.isFinite(qty) || qty <= 0) throw new Error('Cantidad inválida');

    const price = this.prices.get(symbol);
    if (!Number.isFinite(price)) {
      throw new Error(`Sin precio en vivo para ${symbol}. Espera unos segundos o comprueba el símbolo.`);
    }

    const pos = {
      id: this.state.nextId++,
      symbol,
      side,
      qty,
      entryPrice: price,
      openedAt: new Date().toISOString()
    };
    this.state.positions.push(pos);
    this._save();
    this._emit();
    return pos;
  }

  close(id) {
    const idx = this.state.positions.findIndex(p => p.id === Number(id));
    if (idx === -1) throw new Error('Posición no encontrada');
    const pos = this.state.positions[idx];
    const price = this.prices.get(pos.symbol);
    if (!Number.isFinite(price)) throw new Error(`Sin precio en vivo para ${pos.symbol}`);

    const pnl = this._pnl(pos, price);
    this.state.positions.splice(idx, 1);
    this.state.balance += pnl;
    const dia = hoy();
    this.state.realizadoPorDia[dia] = (this.state.realizadoPorDia[dia] || 0) + pnl;
    this.state.history.unshift({
      ...pos,
      exitPrice: price,
      pnl,
      closedAt: new Date().toISOString()
    });
    this.state.history = this.state.history.slice(0, 200);
    this._save();
    this._emit();
    return { ...pos, exitPrice: price, pnl };
  }

  reset() {
    this.state = {
      balanceInicial: this.state.balanceInicial,
      balance: this.state.balanceInicial,
      positions: [],
      history: [],
      realizadoPorDia: {},
      nextId: 1
    };
    this._save();
    this._emit();
  }

  _pnl(pos, price) {
    const dir = pos.side === 'long' ? 1 : -1;
    return (price - pos.entryPrice) * pos.qty * dir;
  }

  snapshot() {
    const dia = hoy();
    const positions = this.state.positions.map(p => {
      const price = this.prices.get(p.symbol);
      const pnl = Number.isFinite(price) ? this._pnl(p, price) : null;
      const pnlPct = Number.isFinite(price)
        ? ((price - p.entryPrice) / p.entryPrice) * 100 * (p.side === 'long' ? 1 : -1)
        : null;
      return { ...p, lastPrice: price ?? null, pnl, pnlPct };
    });
    const flotante = positions.reduce((s, p) => s + (p.pnl || 0), 0);
    const realizadoHoy = this.state.realizadoPorDia[dia] || 0;
    return {
      moneda: this.moneda,
      balance: this.state.balance,
      balanceInicial: this.state.balanceInicial,
      positions,
      history: this.state.history.slice(0, 30),
      realizadoHoy,
      flotante,
      beneficioDia: realizadoHoy + flotante,
      prices: Object.fromEntries(this.prices)
    };
  }
}
