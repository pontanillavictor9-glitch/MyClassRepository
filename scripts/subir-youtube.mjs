// Sube un episodio a YouTube: video, miniatura y subtitulos.
//
//   node scripts/subir-youtube.mjs --auth              (solo autorizar, la primera vez)
//   node scripts/subir-youtube.mjs <carpeta-episodio>  (subir)
//
// Espera en la carpeta del episodio: video-en.mp4, portada.png, audio-en.srt
// y un youtube.json con los metadatos.
//
// Credenciales: client_secret.json en la raiz. El token se guarda en token.json.
// Ambos estan en .gitignore.
//
import { readFileSync, writeFileSync, existsSync, createReadStream, statSync } from 'node:fs'
import { createServer } from 'node:http'
import { execFile } from 'node:child_process'
import { fileURLToPath } from 'node:url'
import { dirname, join, resolve } from 'node:path'
import { google } from 'googleapis'

const root = join(dirname(fileURLToPath(import.meta.url)), '..')
const SECRETO = join(root, 'client_secret.json')
const TOKEN = join(root, 'token.json')

const SCOPES = [
  'https://www.googleapis.com/auth/youtube.upload',
  'https://www.googleapis.com/auth/youtube.force-ssl',
]

function cliente(puerto) {
  const { installed } = JSON.parse(readFileSync(SECRETO, 'utf8'))
  return new google.auth.OAuth2(
    installed.client_id,
    installed.client_secret,
    `http://localhost:${puerto}`,
  )
}

async function autorizar() {
  if (existsSync(TOKEN)) {
    const c = cliente(80)
    c.setCredentials(JSON.parse(readFileSync(TOKEN, 'utf8')))
    return c
  }

  // Servidor local efimero para recoger el codigo de Google.
  return new Promise((ok, mal) => {
    const servidor = createServer()
    servidor.listen(0, async () => {
      const puerto = servidor.address().port
      const c = cliente(puerto)
      const url = c.generateAuthUrl({ access_type: 'offline', scope: SCOPES, prompt: 'consent' })

      console.log('\nAbriendo Opera GX para autorizar.')
      console.log('IMPORTANTE: inicia sesion con la cuenta DEL CANAL.\n')
      console.log(`Si no se abre solo, pega esta URL en el navegador:\n${url}\n`)

      // Se usa Opera GX a proposito: la cuenta del canal esta ahi, no en Chrome.
      const opera = join(process.env.LOCALAPPDATA ?? '', 'Programs', 'Opera GX', 'opera.exe')
      if (existsSync(opera)) execFile(opera, [url], () => {})
      else execFile('cmd', ['/c', 'start', '', url], () => {})

      servidor.on('request', async (req, res) => {
        const codigo = new URL(req.url, `http://localhost:${puerto}`).searchParams.get('code')
        if (!codigo) return
        res.end('Autorizado. Ya puedes cerrar esta pestana y volver a la terminal.')
        servidor.close()
        try {
          const { tokens } = await c.getToken(codigo)
          c.setCredentials(tokens)
          writeFileSync(TOKEN, JSON.stringify(tokens, null, 2), 'utf8')
          console.log('OK  token guardado en token.json (no se sube a GitHub)')
          ok(c)
        } catch (e) {
          mal(e)
        }
      })
    })
  })
}

// La miniatura exige canal verificado por telefono. Si falla, no debe
// impedir que se carguen los subtitulos.
async function ponerExtras(yt, videoId, portada, srt) {
  try {
    await yt.thumbnails.set({ videoId, media: { body: createReadStream(portada) } })
    console.log('OK  miniatura puesta')
  } catch (e) {
    const msg = e?.errors?.[0]?.message ?? e.message
    console.error(`AVISO  miniatura no puesta: ${msg}`)
    console.error('       Verifica el canal en youtube.com/verify y relanza con --extras')
  }
  try {
    await yt.captions.insert({
      part: ['snippet'],
      requestBody: { snippet: { videoId, language: 'en', name: 'English', isDraft: false } },
      media: { body: createReadStream(srt) },
    })
    console.log('OK  subtitulos cargados')
  } catch (e) {
    console.error(`AVISO  subtitulos no cargados: ${e?.errors?.[0]?.message ?? e.message}`)
  }
}

const arg = process.argv[2]
const auth = await autorizar()

// Completa portada y subtitulos de un video ya subido, sin volver a subirlo.
//   node scripts/subir-youtube.mjs --extras <videoId> <carpeta-episodio>
if (arg === '--extras') {
  const videoId = process.argv[3]
  const carpeta = resolve(process.argv[4])
  if (!videoId || !process.argv[4]) {
    console.error('Uso: --extras <videoId> <carpeta-episodio>')
    process.exit(1)
  }
  const yt = google.youtube({ version: 'v3', auth })
  await ponerExtras(yt, videoId, join(carpeta, 'portada.png'), join(carpeta, 'audio-en.srt'))
  process.exit(0)
}

if (arg === '--auth') {
  const yt = google.youtube({ version: 'v3', auth })
  const { data } = await yt.channels.list({ part: ['snippet', 'statistics'], mine: true })
  const canal = data.items?.[0]
  if (!canal) {
    console.error('Autorizado, pero esa cuenta no tiene ningun canal de YouTube.')
    process.exit(1)
  }
  console.log(`\nCanal conectado: ${canal.snippet.title}`)
  console.log(`  id           : ${canal.id}`)
  console.log(`  suscriptores : ${canal.statistics.subscriberCount}`)
  console.log(`  videos       : ${canal.statistics.videoCount}`)
  process.exit(0)
}

if (!arg) {
  console.error('Uso: node scripts/subir-youtube.mjs <carpeta-episodio>  |  --auth')
  process.exit(1)
}

const base = resolve(arg)
const meta = JSON.parse(readFileSync(join(base, 'youtube.json'), 'utf8'))
const video = join(base, 'video-en.mp4')
const portada = join(base, 'portada.png')
const srt = join(base, 'audio-en.srt')

for (const [nombre, ruta] of [['video', video], ['portada', portada], ['subtitulos', srt]]) {
  if (!existsSync(ruta)) {
    console.error(`Falta el ${nombre}: ${ruta}`)
    process.exit(1)
  }
}

const yt = google.youtube({ version: 'v3', auth })
const tam = statSync(video).size

console.log(`Subiendo ${(tam / 1024 / 1024).toFixed(1)} MB...`)

const { data: subido } = await yt.videos.insert(
  {
    part: ['snippet', 'status'],
    requestBody: {
      snippet: {
        title: meta.titulo,
        description: meta.descripcion,
        tags: meta.etiquetas,
        categoryId: meta.categoria ?? '27', // 27 = Education
        defaultLanguage: 'en',
        defaultAudioLanguage: 'en',
      },
      status: {
        privacyStatus: meta.publicarEn ? 'private' : (meta.privacidad ?? 'private'),
        publishAt: meta.publicarEn ?? undefined,
        selfDeclaredMadeForKids: false,
        // Declaracion de contenido generado con IA (voz y dibujos).
        containsSyntheticMedia: meta.contenidoIA ?? true,
        // Permitir incrustar el video en otras webs: alcance extra gratis.
        embeddable: true,
      },
    },
    media: { body: createReadStream(video) },
  },
  {
    onUploadProgress: (e) => {
      const pct = ((e.bytesRead / tam) * 100).toFixed(0)
      process.stdout.write(`\r  ${pct}%   `)
    },
  },
)

console.log(`\nOK  video subido: https://youtu.be/${subido.id}`)

await ponerExtras(yt, subido.id, portada, srt)

console.log(`\nEstado: ${subido.status.privacyStatus}${meta.publicarEn ? ` (programado para ${meta.publicarEn})` : ''}`)
console.log(`Revisalo en https://studio.youtube.com/video/${subido.id}/edit`)
