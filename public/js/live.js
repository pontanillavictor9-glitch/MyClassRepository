// Cliente WebSocket compartido por el panel y los overlays.
// Uso: Live.connect({ onState, onChat, onConfig })

const Live = {
  connect({ onState, onChat, onConfig } = {}) {
    const proto = location.protocol === 'https:' ? 'wss' : 'ws';
    let ws;
    const open = () => {
      ws = new WebSocket(`${proto}://${location.host}/ws`);
      ws.onmessage = ev => {
        try {
          const msg = JSON.parse(ev.data);
          if (msg.type === 'state' && onState) onState(msg.data);
          if (msg.type === 'chat' && onChat) onChat(msg.data);
          if (msg.type === 'config' && onConfig) onConfig(msg.data);
        } catch { /* ignorar */ }
      };
      ws.onclose = () => setTimeout(open, 2000);
    };
    open();
  },

  fmtMoney(n, moneda = 'USD') {
    if (n === null || n === undefined || Number.isNaN(n)) return '—';
    const sign = n > 0 ? '+' : '';
    return sign + n.toLocaleString('es-ES', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }) + (moneda === 'USD' ? ' $' : ' ' + moneda);
  },

  fmtPrice(n) {
    if (!Number.isFinite(n)) return '—';
    const digits = n >= 1000 ? 2 : n >= 1 ? 4 : 6;
    return n.toLocaleString('es-ES', { maximumFractionDigits: digits });
  },

  pnlClass(n) {
    if (n === null || n === undefined) return '';
    return n >= 0 ? 'up' : 'down';
  },

  platformIcon(p) {
    return { twitch: '🟣', youtube: '🔴', tiktok: '⚫' }[p] || '💬';
  }
};
