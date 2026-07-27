// Mini-servidor para ver la tienda en local.
// Arranca con:  npm run tienda   (o doble clic en ver-tienda.bat en Windows)

import path from 'path';
import { fileURLToPath } from 'url';
import express from 'express';

const CARPETA = path.dirname(fileURLToPath(import.meta.url));
const PORT = process.env.TIENDA_PORT || 4000;

const app = express();
app.use(express.static(CARPETA));

app.listen(PORT, () => {
  console.log('');
  console.log('🛍️  Tienda en marcha');
  console.log(`   Abre en tu navegador:  http://localhost:${PORT}/`);
  console.log('');
  console.log('   Edita tienda/js/productos.js para poner tus productos.');
  console.log('   Guía completa del negocio: tienda/README.md');
  console.log('');
});
