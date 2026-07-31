// Extrae de un guion (script-en.md) solo el texto que se locuta:
// las lineas que van despues de "NARRATION:", ignorando VISUAL, titulos y notas.
//
//   node scripts/extract-narration.mjs "ruta/script-en.md"            -> imprime el texto
//   node scripts/extract-narration.mjs "ruta/script-en.md" --out x.txt -> lo guarda
//
import { readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

const guion = process.argv[2]
if (!guion) {
  console.error('Uso: node scripts/extract-narration.mjs <script-en.md> [--out salida.txt]')
  process.exit(1)
}

const lineas = readFileSync(resolve(guion), 'utf8').split(/\r?\n/)
const bloques = []
let actual = null

for (const linea of lineas) {
  const t = linea.trim()

  if (t === 'NARRATION:') {
    actual = []
    bloques.push(actual)
    continue
  }

  // Cualquiera de estas marcas cierra el bloque de narracion.
  if (actual && (t.startsWith('#') || t.startsWith('VISUAL:') || t.startsWith('---'))) {
    actual = null
    continue
  }

  if (actual && t) actual.push(t)
}

const texto = bloques
  .map((b) => b.join('\n'))
  .filter(Boolean)
  .join('\n\n')

const salida = process.argv.includes('--out') ? process.argv[process.argv.indexOf('--out') + 1] : null

if (salida) {
  writeFileSync(resolve(salida), texto, 'utf8')
  const palabras = texto.split(/\s+/).filter(Boolean).length
  console.log(`OK  ${salida}`)
  console.log(`    ${bloques.length} bloques  |  ${palabras} palabras  |  ${texto.length} caracteres`)
  console.log(`    duracion estimada: ~${Math.round(palabras / 150)} min a ritmo conversacional`)
} else {
  console.log(texto)
}
