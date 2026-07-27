// Chat de Twitch por IRC anónimo sobre WebSocket. No requiere credenciales
// para LEER el chat de un canal público.

import WebSocket from 'ws';

const TWITCH_IRC = 'wss://irc-ws.chat.twitch.tv:443';

export function startTwitchChat(canal, onMessage) {
  if (!canal) return;
  canal = canal.toLowerCase().replace(/^#/, '');
  let ws;
  let retry = 2000;

  const connect = () => {
    try {
      ws = new WebSocket(TWITCH_IRC);
    } catch (err) {
      console.error('[twitch] Error creando WebSocket:', err.message);
      setTimeout(connect, retry);
      retry = Math.min(retry * 2, 60000);
      return;
    }

    ws.on('open', () => {
      retry = 2000;
      const anon = 'justinfan' + Math.floor(Math.random() * 100000);
      ws.send('CAP REQ :twitch.tv/tags');
      ws.send('PASS SCHMOOPIIE');
      ws.send(`NICK ${anon}`);
      ws.send(`JOIN #${canal}`);
      console.log(`[twitch] Conectado al chat de #${canal} (lectura anónima)`);
    });

    ws.on('message', raw => {
      const lines = raw.toString().split('\r\n').filter(Boolean);
      for (const line of lines) {
        if (line.startsWith('PING')) {
          ws.send('PONG :tmi.twitch.tv');
          continue;
        }
        const m = line.match(/^(?:@([^ ]+) )?:([^!]+)![^ ]+ PRIVMSG #[^ ]+ :(.*)$/);
        if (!m) continue;
        const tags = {};
        if (m[1]) {
          for (const kv of m[1].split(';')) {
            const [k, v] = kv.split('=');
            tags[k] = v;
          }
        }
        onMessage({
          platform: 'twitch',
          user: tags['display-name'] || m[2],
          text: m[3],
          color: tags.color || null,
          ts: Date.now()
        });
      }
    });

    ws.on('close', () => {
      console.warn('[twitch] Desconectado, reintentando...');
      setTimeout(connect, retry);
      retry = Math.min(retry * 2, 60000);
    });

    ws.on('error', err => {
      console.error('[twitch] Error:', err.message);
      try { ws.close(); } catch { /* ya cerrado */ }
    });
  };

  connect();
}
