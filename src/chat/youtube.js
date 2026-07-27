// Chat de YouTube Live usando la librería youtube-chat (no requiere API key).
// Acepta un handle ("@MiCanal"), un channelId ("UC...") o un liveId (id del vídeo).

import { LiveChat } from 'youtube-chat';

export async function startYouTubeChat(canal, onMessage) {
  if (!canal) return;

  let id;
  if (canal.startsWith('@')) id = { handle: canal };
  else if (canal.startsWith('UC')) id = { channelId: canal };
  else id = { liveId: canal };

  const RETRY_MS = 30000;
  const chat = new LiveChat(id);

  chat.on('chat', item => {
    const text = item.message
      .map(m => ('text' in m ? m.text : m.emojiText || ''))
      .join('');
    onMessage({
      platform: 'youtube',
      user: item.author.name,
      text,
      color: null,
      superchat: item.superchat ? item.superchat.amount : null,
      isOwner: item.isOwner,
      isModerator: item.isModerator,
      ts: Date.now()
    });
  });

  chat.on('error', err => {
    console.error('[youtube] Error:', err?.message || err);
  });

  chat.on('end', () => {
    console.warn(`[youtube] Directo finalizado o no encontrado. Reintento en ${RETRY_MS / 1000}s...`);
    setTimeout(() => intentar(), RETRY_MS);
  });

  const intentar = async () => {
    try {
      const ok = await chat.start();
      if (ok) {
        console.log(`[youtube] Conectado al chat en directo de ${canal}`);
      } else {
        console.warn(`[youtube] No hay directo activo en ${canal}. Reintento en ${RETRY_MS / 1000}s...`);
        setTimeout(intentar, RETRY_MS);
      }
    } catch (err) {
      console.error('[youtube] No se pudo conectar:', err?.message || err);
      setTimeout(intentar, RETRY_MS);
    }
  };

  intentar();
}
