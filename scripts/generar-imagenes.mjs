// Genera con Higgsfield una imagen por escena y la descarga a la carpeta del episodio.
//
//   node scripts/generar-imagenes.mjs <escenas-imagen.json> <carpeta-salida> [--modelo z_image]
//
// Reanudable: si la imagen NN ya existe en la carpeta, se salta.
//
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs'
import { execFileSync } from 'node:child_process'
import { resolve, join } from 'node:path'

const escenasRuta = process.argv[2]
const carpeta = process.argv[3]
if (!escenasRuta || !carpeta) {
  console.error('Uso: node scripts/generar-imagenes.mjs <escenas-imagen.json> <carpeta> [--modelo z_image]')
  process.exit(1)
}
const iM = process.argv.indexOf('--modelo')
const modelo = iM === -1 ? 'z_image' : process.argv[iM + 1]

const ESTILO =
  'Extremely simple beginner drawing made in MS Paint by someone who is not good at drawing. ' +
  'All people must be simple STICK FIGURES: plain white round head with a black outline, two dot eyes, ' +
  'a simple line mouth, thin line arms and legs. Do not draw realistic or cartoon children, no skin tones, ' +
  'no rounded cartoon bodies. Thick uneven black outlines, wobbly hand-drawn lines. Clothes and objects are ' +
  'filled with flat solid colors like a paint bucket fill. No gradients, no shading, no 3D, no cinematic ' +
  'lighting, no polished illustration, no vector art. Plain white background with lots of empty space. ' +
  'Amateur, funny, intentionally bad. Scene: '

// En Windows, Node se niega a ejecutar el .cmd (EINVAL) y no encuentra el
// nombre sin extension (ENOENT). Se llama al .js directamente con Node.
const cliJs = process.env.APPDATA
  ? join(process.env.APPDATA, 'npm', 'node_modules', '@higgsfield', 'cli', 'bin', 'higgsfield.js')
  : null
const usarNode = cliJs && existsSync(cliJs)
const ejecutable = usarNode ? process.execPath : 'higgsfield'
const prefijo = usarNode ? [cliJs] : []

const escenas = JSON.parse(readFileSync(resolve(escenasRuta), 'utf8'))
mkdirSync(resolve(carpeta), { recursive: true })

for (const [i, escena] of escenas.entries()) {
  const n = String(i + 1).padStart(2, '0')
  const destino = join(resolve(carpeta), `${n}.png`)
  if (existsSync(destino)) {
    console.log(`${n}  ya existe, saltando`)
    continue
  }
  try {
    const salida = execFileSync(
      ejecutable,
      [...prefijo, 'generate', 'create', modelo, '--aspect_ratio', '16:9', '--prompt', ESTILO + escena, '--wait', '--wait-timeout', '8m'],
      { encoding: 'utf8', maxBuffer: 10 * 1024 * 1024 },
    )
    const url = salida.trim().split('\n').filter((l) => l.startsWith('http')).pop()
    if (!url) throw new Error(`sin URL en la respuesta: ${salida.slice(0, 200)}`)
    const res = await fetch(url)
    writeFileSync(destino, Buffer.from(await res.arrayBuffer()))
    console.log(`${n}  OK`)
  } catch (e) {
    console.error(`${n}  FALLO: ${String(e.message).slice(0, 200)}`)
  }
}

console.log('\nTerminado.')
