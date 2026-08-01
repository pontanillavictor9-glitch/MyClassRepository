// Lee las metricas de los videos del canal.
//
//   node scripts/metricas.mjs           (stats basicas + analytics si hay permiso)
//   node scripts/metricas.mjs --auth    (re-autorizar anadiendo el permiso de Analytics)
//
// Las stats basicas (visitas, likes, comentarios) salen de la Data API y
// funcionan con el token de subida. La retencion y el CTR de portada salen de
// la Analytics API y necesitan el scope yt-analytics.readonly: si falta, hay
// que pasar --auth una vez.
//
import { readFileSync, writeFileSync, existsSync } from 'node:fs'
import { createServer } from 'node:http'
import { execFile } from 'node:child_process'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'
import { google } from 'googleapis'

const root = join(dirname(fileURLToPath(import.meta.url)), '..')
const SECRETO = join(root, 'client_secret.json')
const TOKEN = join(root, 'token.json')

const SCOPES = [
  'https://www.googleapis.com/auth/youtube.upload',
  'https://www.googleapis.com/auth/youtube.force-ssl',
  'https://www.googleapis.com/auth/yt-analytics.readonly',
]

function cliente(puerto) {
  const { installed } = JSON.parse(readFileSync(SECRETO, 'utf8'))
  return new google.auth.OAuth2(
    installed.client_id,
    installed.client_secret,
    `http://localhost:${puerto}`,
  )
}

async function reautorizar() {
  return new Promise((ok, mal) => {
    const servidor = createServer()
    servidor.listen(0, async () => {
      const puerto = servidor.address().port
      const c = cliente(puerto)
      const url = c.generateAuthUrl({ access_type: 'offline', scope: SCOPES, prompt: 'consent' })

      console.log('\nAutoriza con la cuenta DEL CANAL (zhaaall1234@gmail.com).')
      console.log(`Si no se abre solo, pega esta URL:\n${url}\n`)

      const opera = join(process.env.LOCALAPPDATA ?? '', 'Programs', 'Opera GX', 'opera.exe')
      if (existsSync(opera)) execFile(opera, [url], () => {})
      else execFile('cmd', ['/c', 'start', '', url], () => {})

      servidor.on('request', async (req, res) => {
        const code = new URL(req.url, `http://localhost:${puerto}`).searchParams.get('code')
        res.end('Listo. Puedes cerrar esta pestana.')
        servidor.close()
        if (!code) return mal(new Error('sin codigo'))
        const { tokens } = await c.getToken(code)
        writeFileSync(TOKEN, JSON.stringify(tokens, null, 2))
        c.setCredentials(tokens)
        console.log('Token guardado con permiso de Analytics.')
        ok(c)
      })
    })
  })
}

function tokenGuardado() {
  const c = cliente(80)
  c.setCredentials(JSON.parse(readFileSync(TOKEN, 'utf8')))
  return c
}

const auth = process.argv.includes('--auth') ? await reautorizar() : tokenGuardado()

const youtube = google.youtube({ version: 'v3', auth })
const analytics = google.youtubeAnalytics({ version: 'v2', auth })

// 1. Todos los videos del canal (los programados incluidos).
const canal = await youtube.channels.list({ part: ['contentDetails', 'statistics'], mine: true })
const subs = canal.data.items[0].statistics
const subidas = canal.data.items[0].contentDetails.relatedPlaylists.uploads

const lista = await youtube.playlistItems.list({
  part: ['contentDetails'], playlistId: subidas, maxResults: 50,
})
const ids = lista.data.items.map((i) => i.contentDetails.videoId)

const vids = await youtube.videos.list({
  part: ['snippet', 'statistics', 'status', 'contentDetails'], id: ids,
})

console.log(`\nCANAL: ${subs.subscriberCount} subs, ${subs.viewCount} visitas totales, ${subs.videoCount} videos publicos\n`)

const publicos = []
for (const v of vids.data.items) {
  const s = v.statistics
  const estado = v.status.privacyStatus === 'private' && v.status.publishAt
    ? `programado ${v.status.publishAt.slice(0, 16).replace('T', ' ')}`
    : v.status.privacyStatus
  console.log(`${v.id}  ${estado.padEnd(24)}  ${(s.viewCount ?? '0').padStart(6)} visitas  ${(s.likeCount ?? '0').padStart(4)} likes  ${(s.commentCount ?? '0').padStart(3)} coment.  ${v.snippet.title}`)
  if (v.status.privacyStatus === 'public') publicos.push(v)
}

if (!publicos.length) {
  console.log('\nNingun video publico todavia: no hay analytics que mirar.')
  process.exit(0)
}

// 2. Retencion, CTR y origen de las visitas de los que ya estan publicos.
const hoy = new Date().toISOString().slice(0, 10)
const desde = '2026-07-01'

async function informe(opciones) {
  try {
    const r = await analytics.reports.query({
      ids: 'channel==MINE', startDate: desde, endDate: hoy, ...opciones,
    })
    return r.data
  } catch (e) {
    const msg = e?.errors?.[0]?.message ?? e.message
    if (/insufficient|scope|forbidden/i.test(msg)) {
      console.log(`\nFalta permiso de Analytics. Ejecuta:\n  node scripts/metricas.mjs --auth\n`)
      process.exit(1)
    }
    console.log(`  (error: ${msg})`)
    return null
  }
}

console.log('\n--- RETENCION Y CLICS (desde ' + desde + ') ---\n')

const porVideo = await informe({
  dimensions: 'video',
  metrics: 'views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained',
  filters: 'video==' + publicos.map((v) => v.id).join(','),
})

if (porVideo?.rows) {
  const titulo = Object.fromEntries(publicos.map((v) => [v.id, v.snippet.title]))
  for (const [id, views, min, dur, pct, subsG] of porVideo.rows) {
    console.log(`${titulo[id]}`)
    console.log(`  ${views} visitas | ${min} min vistos | duracion media ${Math.floor(dur / 60)}:${String(dur % 60).padStart(2, '0')} | retencion ${pct.toFixed(1)}% | +${subsG} subs\n`)
  }
}

const impresiones = await informe({
  dimensions: 'video',
  metrics: 'impressions,impressionClickThroughRate',
  filters: 'video==' + publicos.map((v) => v.id).join(','),
})
if (impresiones?.rows) {
  console.log('CLICS EN LA PORTADA:')
  const titulo = Object.fromEntries(publicos.map((v) => [v.id, v.snippet.title]))
  for (const [id, imp, ctr] of impresiones.rows) {
    console.log(`  ${String(imp).padStart(6)} impresiones  CTR ${ctr.toFixed(2)}%  ${titulo[id]}`)
  }
}

const origen = await informe({
  dimensions: 'insightTrafficSourceType', metrics: 'views,estimatedMinutesWatched', sort: '-views',
})
if (origen?.rows) {
  console.log('\nORIGEN DE LAS VISITAS:')
  for (const [fuente, views, min] of origen.rows) {
    console.log(`  ${String(views).padStart(5)} visitas  ${String(min).padStart(5)} min  ${fuente}`)
  }
}
