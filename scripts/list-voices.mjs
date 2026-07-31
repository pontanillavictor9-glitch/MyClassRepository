// Lista las voces disponibles en la cuenta de ElevenLabs.
// Lee la API key del archivo .env (que nunca se sube a GitHub) y NUNCA la imprime.
//
//   node scripts/list-voices.mjs
//
import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

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

const res = await fetch('https://api.elevenlabs.io/v1/voices', {
  headers: { 'xi-api-key': leerApiKey() },
})

if (!res.ok) {
  console.error(`Error ${res.status} de ElevenLabs: ${await res.text()}`)
  process.exit(1)
}

const { voices } = await res.json()
console.log(`${voices.length} voces en la cuenta:\n`)

for (const v of voices) {
  const etiquetas = Object.values(v.labels ?? {}).filter(Boolean).join(', ')
  console.log(`  ${v.name}`)
  console.log(`    voice_id : ${v.voice_id}`)
  console.log(`    tipo     : ${v.category}${etiquetas ? `  |  ${etiquetas}` : ''}`)
  if (v.description) console.log(`    describe : ${v.description}`)
  if (v.preview_url) console.log(`    escuchar : ${v.preview_url}`)
  console.log()
}
