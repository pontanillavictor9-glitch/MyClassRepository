// Reparte los planos por PARRAFO en vez de por duracion fija.
// Pensado para guiones que ya vienen con los planos decididos (un parrafo,
// un plano), como los de Archivo Rojo.
//
//   node scripts/agrupar-parrafos.mjs <audio-en-timestamps.json> <narracion.txt>
//
// Usa la alineacion caracter a caracter para saber en que segundo empieza y
// acaba cada parrafo del texto original.
//
import { readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

const rutaTs = process.argv[2]
const rutaTexto = process.argv[3]
if (!rutaTs || !rutaTexto) {
  console.error('Uso: node scripts/agrupar-parrafos.mjs <timestamps.json> <narracion.txt>')
  process.exit(1)
}

const { alignment, duracion, frases } = JSON.parse(readFileSync(resolve(rutaTs), 'utf8'))
const texto = readFileSync(resolve(rutaTexto), 'utf8')

// El JSON de tts-timestamps guarda frases, no la alineacion cruda. Se
// reconstruye la posicion de cada parrafo contando caracteres no vacios.
const parrafos = texto.split(/\n\s*\n/).map((p) => p.trim()).filter(Boolean)

// Mapa: para cada parrafo, cuantos caracteres visibles lleva acumulados el texto.
const norm = (s) => s.replace(/\s+/g, ' ').trim()
let cursor = 0
const escenas = []

for (const p of parrafos) {
  const objetivo = norm(p)
  let acumulado = ''
  const inicioFrase = cursor
  while (cursor < frases.length && norm(acumulado).length < objetivo.length - 5) {
    acumulado += (acumulado ? ' ' : '') + frases[cursor].texto
    cursor++
  }
  if (cursor === inicioFrase) continue
  escenas.push({
    inicio: frases[inicioFrase].inicio,
    fin: frases[cursor - 1].fin,
    texto: acumulado,
  })
}

// El ultimo plano se estira hasta el final del audio por si sobran decimas.
if (escenas.length) escenas[escenas.length - 1].fin = duracion

const salida = resolve(rutaTs).replace(/-timestamps\.json$/, '-escenas.json')
writeFileSync(salida, JSON.stringify({ duracion, escenas }, null, 2), 'utf8')

console.log(`${parrafos.length} parrafos -> ${escenas.length} planos`)
console.log(`Guardado en ${salida}\n`)
for (const [n, e] of escenas.entries()) {
  const m = Math.floor(e.inicio / 60)
  const s = String(Math.floor(e.inicio % 60)).padStart(2, '0')
  console.log(`${String(n + 1).padStart(2)}. [${m}:${s}] (${(e.fin - e.inicio).toFixed(0)}s) ${e.texto.slice(0, 90)}`)
}
