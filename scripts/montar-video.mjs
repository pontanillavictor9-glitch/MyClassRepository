// Monta el video final: una imagen por escena, cada una desde su segundo
// hasta el siguiente, con el audio encima.
//
//   node scripts/montar-video.mjs <carpeta-episodio>
//
// Espera encontrar dentro de la carpeta:
//   audio-en.mp3, audio-en-escenas.json, imagenes/01.png ... NN.png
//
import { readFileSync, writeFileSync, existsSync } from 'node:fs'
import { execFileSync } from 'node:child_process'
import { resolve, join } from 'node:path'

const carpeta = process.argv[2]
if (!carpeta) {
  console.error('Uso: node scripts/montar-video.mjs <carpeta-episodio>')
  process.exit(1)
}
const base = resolve(carpeta)
const audio = join(base, 'audio-en.mp3')
const escenasJson = join(base, 'audio-en-escenas.json')
const imgDir = join(base, 'imagenes')
const salida = join(base, 'video-en.mp4')

const { escenas } = JSON.parse(readFileSync(escenasJson, 'utf8'))

// Comprobar que estan todas las imagenes antes de empezar.
const faltan = []
for (let i = 0; i < escenas.length; i++) {
  const p = join(imgDir, `${String(i + 1).padStart(2, '0')}.png`)
  if (!existsSync(p)) faltan.push(i + 1)
}
if (faltan.length) {
  console.error(`Faltan imagenes: ${faltan.join(', ')}`)
  process.exit(1)
}

// Lista para el demuxer concat. La ultima entrada se repite: lo exige ffmpeg.
const lineas = []
for (let i = 0; i < escenas.length; i++) {
  const p = join(imgDir, `${String(i + 1).padStart(2, '0')}.png`).replace(/\\/g, '/')
  const dur = escenas[i].fin - escenas[i].inicio
  lineas.push(`file '${p}'`, `duration ${dur.toFixed(3)}`)
}
lineas.push(`file '${join(imgDir, `${String(escenas.length).padStart(2, '0')}.png`).replace(/\\/g, '/')}'`)

const lista = join(base, 'concat.txt')
writeFileSync(lista, lineas.join('\n'), 'utf8')

console.log(`Montando ${escenas.length} escenas...`)

execFileSync(
  'ffmpeg',
  [
    '-v', 'error', '-stats', '-y',
    '-f', 'concat', '-safe', '0', '-i', lista,
    '-i', audio,
    '-vf', 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:white,format=yuv420p',
    '-r', '30',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
    '-c:a', 'aac', '-b:a', '192k',
    '-shortest',
    salida,
  ],
  { stdio: 'inherit' },
)

const dur = execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', salida], { encoding: 'utf8' }).trim()
const seg = Math.round(Number(dur))
console.log(`\nOK  ${salida}`)
console.log(`    duracion ${Math.floor(seg / 60)}:${String(seg % 60).padStart(2, '0')}`)
