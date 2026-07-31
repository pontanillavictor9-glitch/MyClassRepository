// Genera el audio de un episodio Y sus marcas de tiempo en una sola llamada.
// Sustituye por completo el paso de TurboScribe.
// Lee la API key del .env y NUNCA la imprime.
//
//   node scripts/tts-timestamps.mjs --text-file narracion.txt --out carpeta/audio-en.mp3
//
// Escribe dos archivos: el mp3, y un .json con los tiempos de cada frase.
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

function arg(nombre, porDefecto) {
  const i = process.argv.indexOf(`--${nombre}`)
  return i === -1 ? porDefecto : process.argv[i + 1]
}

const salida = arg('out')
const textoRuta = arg('text-file')
const voiceId = arg('voice', 'TX3LPaxmHKxFdv7VOQHJ') // Liam, voz del canal EN

if (!salida || !textoRuta) {
  console.error('Uso: --text-file <narracion.txt> --out <audio.mp3> [--voice <id>]')
  process.exit(1)
}

const texto = readFileSync(resolve(textoRuta), 'utf8')

const res = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voiceId}/with-timestamps?output_format=mp3_44100_128`, {
  method: 'POST',
  headers: { 'xi-api-key': leerApiKey(), 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: texto,
    model_id: 'eleven_multilingual_v2',
    voice_settings: {
      stability: Number(arg('stability', 0.5)),
      similarity_boost: Number(arg('similarity', 0.75)),
      style: 0.0,
      use_speaker_boost: true,
      // Menos de 1 = mas lento. Util para narracion documental.
      speed: Number(arg('speed', 1.0)),
    },
  }),
})

if (!res.ok) {
  console.error(`Error ${res.status} de ElevenLabs: ${(await res.text()).slice(0, 400)}`)
  process.exit(1)
}

const datos = await res.json()
const audio = Buffer.from(datos.audio_base64, 'base64')
mkdirSync(dirname(resolve(salida)), { recursive: true })
writeFileSync(resolve(salida), audio)

// Reconstruir frases a partir de la alineacion caracter a caracter.
const al = datos.alignment
const chars = al.characters
const ini = al.character_start_times_seconds
const fin = al.character_end_times_seconds

const frases = []
let actual = { texto: '', inicio: ini[0] ?? 0, fin: 0 }

for (let i = 0; i < chars.length; i++) {
  actual.texto += chars[i]
  actual.fin = fin[i]
  // Corta en fin de frase, pero no en los puntos suspensivos.
  const esFinal = /[.!?]/.test(chars[i]) && chars[i + 1] !== '.' && chars[i - 1] !== '.'
  const siguienteEsEspacio = i + 1 >= chars.length || /\s/.test(chars[i + 1])
  if ((esFinal && siguienteEsEspacio) || i === chars.length - 1) {
    const limpio = actual.texto.trim()
    if (limpio) frases.push({ inicio: +actual.inicio.toFixed(2), fin: +actual.fin.toFixed(2), texto: limpio })
    actual = { texto: '', inicio: fin[i], fin: fin[i] }
  }
}

const rutaJson = resolve(salida).replace(/\.mp3$/, '') + '-timestamps.json'
writeFileSync(rutaJson, JSON.stringify({ duracion: fin[fin.length - 1], frases }, null, 2), 'utf8')

const dur = fin[fin.length - 1]
console.log(`OK  ${salida}  (${(audio.length / 1024 / 1024).toFixed(1)} MB)`)
console.log(`OK  ${rutaJson}`)
console.log(`    ${texto.length} caracteres facturados`)
console.log(`    ${frases.length} frases  |  duracion ${Math.floor(dur / 60)}:${String(Math.round(dur % 60)).padStart(2, '0')}`)
