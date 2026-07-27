// Chat de TikTok Live usando tiktok-live-connector (no requiere credenciales).
// Solo funciona mientras el usuario está EN DIRECTO en TikTok.

import pkg from 'tiktok-live-connector';
const { WebcastPushConnection } = pkg;

export function startTikTokChat(usuario, onMessage) {
  if (!usuario) return;
  usuario = usuario.replace(/^@/, '');

  const RETRY_MS = 30000;
  const conn = new WebcastPushConnection(usuario, { enableExtendedGiftInfo: false });

  conn.on('chat', data => {
    onMessage({
      platform: 'tiktok',
      user: data.nickname || data.uniqueId,
      text: data.comment,
      color: null,
      ts: Date.now()
    });
  });

  conn.on('disconnected', () => {
    console.warn(`[tiktok] Desconectado. Reintento en ${RETRY_MS / 1000}s...`);
    setTimeout(conectar, RETRY_MS);
  });

  conn.on('error', err => {
    console.error('[tiktok] Error:', err?.info || err?.message || err);
  });

  const conectar = () => {
    conn.connect()
      .then(state => {
        console.log(`[tiktok] Conectado al directo de @${usuario} (roomId ${state.roomId})`);
      })
      .catch(err => {
        console.warn(`[tiktok] No hay directo activo en @${usuario} (${err?.message || err}). Reintento en ${RETRY_MS / 1000}s...`);
        setTimeout(conectar, RETRY_MS);
      });
  };

  conectar();
}
