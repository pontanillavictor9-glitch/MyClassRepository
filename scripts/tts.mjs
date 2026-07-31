// Genera audio con ElevenLabs a partir de texto.
// Lee la API key del archivo .env (nunca se sube a GitHub) y NUNCA la imprime.
//
//   node scripts/tts.mjs --voice <voice_id> --out ruta/salida.mp3 --text "texto"
//   node scripts/tts.mjs --voice <voice_id> --out ruta/salida.mp3 --text-file ruta/texto.txt
//
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join, resolve } from 'node:path'

const root = join(dirname(fileURLToPath(import.meta.url)), '..')

function leerApiKey() {
  if (process.env.ELEVENLABS_API_KEY) return process.env.ELEVENLABS_API_KEY
  let env
  try {
    env = readFileSync(join(root, '.env'), 'utf8')
  } catch {
    console.error('No encuentro el archivo .env en la raiz del repositorio.')
    process.exit(1)
  }
  const linea = env.split('\n').find((l) => l.trim().startsWith('ELEVENLABS_API_KEY='))
  if (!linea) {
    console.error('El .env existe pero no tiene la linea ELEVENLABS_API_KEY=...')
    process.exit(1)
  }
  return linea.split('=').slice(1).join('=').trim().replace(/^["']|["']$/g, '')
}

function arg(nombre) {
  const i = process.argv.indexOf(`--${nombre}`)
  return i === -1 ? undefined : process.argv[i + 1]
}

const voiceId = arg('voice')
const salida = arg('out')
const texto = arg('text') ?? (arg('text-file') ? readFileSync(resolve(arg('text-file')), 'utf8') : undefined)

if (!voiceId || !salida || !texto) {
  console.error('Faltan argumentos. Uso: --voice <id> --out <archivo.mp3> --text "..." | --text-file <archivo>')
  process.exit(1)
}

// Modelo multilingue: misma voz reutilizable en otros idiomas.
const modelo = arg('model') ?? 'eleven_multilingual_v2'

const res = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voiceId}?output_format=mp3_44100_128`, {
  method: 'POST',
  headers: { 'xi-api-key': leerApiKey(), 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: texto,
    model_id: modelo,
    voice_settings: {
      stability: 0.5,
      similarity_boost: 0.75,
      style: 0.0,
      use_speaker_boost: true,
    },
  }),
})

if (!res.ok) {
  console.error(`Error ${res.status} de ElevenLabs: ${await res.text()}`)
  process.exit(1)
}

const audio = Buffer.from(await res.arrayBuffer())
mkdirSync(dirname(resolve(salida)), { recursive: true })
writeFileSync(resolve(salida), audio)
console.log(`OK  ${salida}  (${(audio.length / 1024).toFixed(0)} KB, ${texto.length} caracteres facturados)`)
