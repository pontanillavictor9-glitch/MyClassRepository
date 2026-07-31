// Convierte las frases cronometradas de ElevenLabs en un archivo .srt
// listo para subir a YouTube como subtitulos.
//
//   node scripts/generar-srt.mjs <audio-en-timestamps.json>
//
import { readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

const ruta = process.argv[2]
if (!ruta) {
  console.error('Uso: node scripts/generar-srt.mjs <audio-en-timestamps.json>')
  process.exit(1)
}

const { frases } = JSON.parse(readFileSync(resolve(ruta), 'utf8'))

function tiempo(s) {
  const h = Math.floor(s / 3600)
  const m = Math.floor((s % 3600) / 60)
  const seg = Math.floor(s % 60)
  const ms = Math.round((s - Math.floor(s)) * 1000)
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}:${String(seg).padStart(2, '0')},${String(ms).padStart(3, '0')}`
}

// Las frases largas se parten en dos lineas para que se lean bien en pantalla.
function partir(texto) {
  if (texto.length <= 42) return texto
  const palabras = texto.split(' ')
  const mitad = Math.ceil(palabras.length / 2)
  return palabras.slice(0, mitad).join(' ') + '\n' + palabras.slice(mitad).join(' ')
}

const bloques = frases.map((f, i) =>
  `${i + 1}\n${tiempo(f.inicio)} --> ${tiempo(f.fin)}\n${partir(f.texto)}\n`,
)

const salida = resolve(ruta).replace(/-timestamps\.json$/, '.srt')
writeFileSync(salida, bloques.join('\n'), 'utf8')
console.log(`OK  ${salida}  (${frases.length} subtitulos)`)
