// Agrupa las frases cronometradas en escenas de duracion objetivo,
// para que a cada escena le corresponda una imagen.
//
//   node scripts/agrupar-escenas.mjs <audio-en-timestamps.json> [--segundos 14]
//
import { readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

const ruta = process.argv[2]
if (!ruta) {
  console.error('Uso: node scripts/agrupar-escenas.mjs <timestamps.json> [--segundos 14]')
  process.exit(1)
}
const i = process.argv.indexOf('--segundos')
const objetivo = i === -1 ? 14 : Number(process.argv[i + 1])

const { duracion, frases } = JSON.parse(readFileSync(resolve(ruta), 'utf8'))

const escenas = []
let actual = null

for (const f of frases) {
  if (!actual) actual = { inicio: f.inicio, fin: f.fin, texto: f.texto }
  else {
    actual.fin = f.fin
    actual.texto += ' ' + f.texto
  }
  if (actual.fin - actual.inicio >= objetivo) {
    escenas.push(actual)
    actual = null
  }
}
if (actual) {
  // La ultima escena corta se pega a la anterior para no dejar un plano de 2s.
  if (escenas.length && actual.fin - actual.inicio < objetivo / 2) {
    const ult = escenas[escenas.length - 1]
    ult.fin = actual.fin
    ult.texto += ' ' + actual.texto
  } else escenas.push(actual)
}

const salida = resolve(ruta).replace(/-timestamps\.json$/, '-escenas.json')
writeFileSync(salida, JSON.stringify({ duracion, escenas }, null, 2), 'utf8')

console.log(`${escenas.length} escenas  (objetivo ${objetivo}s, duracion total ${Math.floor(duracion / 60)}:${String(Math.round(duracion % 60)).padStart(2, '0')})`)
console.log(`Guardado en ${salida}\n`)
for (const [n, e] of escenas.entries()) {
  const m = Math.floor(e.inicio / 60)
  const s = String(Math.floor(e.inicio % 60)).padStart(2, '0')
  console.log(`${String(n + 1).padStart(2)}. [${m}:${s}] (${(e.fin - e.inicio).toFixed(0)}s) ${e.texto}`)
}
