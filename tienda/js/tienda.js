// Lógica de la tienda monoproducto: landing (index.html) y carrito (carrito.html).
// El carrito se guarda en localStorage, así sobrevive a recargas de página.

import { PRODUCTOS, TIENDA, LANDING } from './productos.js';

const CLAVE_CARRITO = 'tienda-carrito';

// ---------- Carrito (localStorage) ----------

function leerCarrito() {
  try {
    return JSON.parse(localStorage.getItem(CLAVE_CARRITO)) || {};
  } catch {
    return {};
  }
}

function guardarCarrito(carrito) {
  localStorage.setItem(CLAVE_CARRITO, JSON.stringify(carrito));
  pintarContador();
}

export function agregarAlCarrito(id, cantidad = 1) {
  const carrito = leerCarrito();
  carrito[id] = (carrito[id] || 0) + cantidad;
  guardarCarrito(carrito);
}

export function cambiarCantidad(id, delta) {
  const carrito = leerCarrito();
  carrito[id] = (carrito[id] || 0) + delta;
  if (carrito[id] <= 0) delete carrito[id];
  guardarCarrito(carrito);
}

export function quitarDelCarrito(id) {
  const carrito = leerCarrito();
  delete carrito[id];
  guardarCarrito(carrito);
}

function unidadesTotales() {
  return Object.values(leerCarrito()).reduce((suma, n) => suma + n, 0);
}

export function precio(n) {
  return n.toFixed(2).replace('.', ',') + ' ' + TIENDA.moneda;
}

// ---------- Elementos comunes ----------

export function pintarContador() {
  document.querySelectorAll('.contador-carrito').forEach(el => {
    el.textContent = unidadesTotales();
  });
}

export function iniciarPagina() {
  const barra = document.querySelector('.barra-envio');
  if (barra) barra.textContent = TIENDA.oferta;
  pintarContador();
}

function estrellas(n) {
  return '★'.repeat(n) + '☆'.repeat(5 - n);
}

// ---------- Landing (index.html) ----------

export function pintarLanding() {
  // Galería del héroe
  const principal = document.getElementById('imagen-principal');
  const miniaturas = document.getElementById('miniaturas');
  principal.src = LANDING.galeria[0];
  miniaturas.innerHTML = LANDING.galeria
    .map((src, i) => `<img src="${src}" data-src="${src}" class="${i === 0 ? 'activa' : ''}" alt="Vista ${i + 1}">`)
    .join('');
  miniaturas.addEventListener('click', ev => {
    if (!ev.target.dataset.src) return;
    principal.src = ev.target.dataset.src;
    miniaturas.querySelectorAll('img').forEach(m => m.classList.remove('activa'));
    ev.target.classList.add('activa');
  });

  // Selector de packs
  const cajaPacks = document.getElementById('packs');
  let packElegido = PRODUCTOS[1] ? PRODUCTOS[1].id : PRODUCTOS[0].id; // el "más vendido" por defecto
  function pintarPacks() {
    cajaPacks.innerHTML = PRODUCTOS.map(p => `
      <label class="pack ${p.id === packElegido ? 'elegido' : ''}" data-pack="${p.id}">
        <span class="radio"></span>
        <span class="pack-info">
          <strong>${p.nombre}</strong>
          <small>${p.nota}</small>
        </span>
        <span class="pack-precio">
          <s>${precio(p.precioAntes)}</s>
          <strong>${precio(p.precio)}</strong>
        </span>
      </label>
    `).join('');
  }
  pintarPacks();
  cajaPacks.addEventListener('click', ev => {
    const pack = ev.target.closest('[data-pack]');
    if (!pack) return;
    packElegido = pack.dataset.pack;
    pintarPacks();
  });

  document.getElementById('comprar').addEventListener('click', () => {
    agregarAlCarrito(packElegido);
    location.href = 'carrito.html';
  });

  // Sellos de garantía bajo el botón
  document.getElementById('sellos').innerHTML = LANDING.garantias
    .map(g => `<span>✓ ${g}</span>`)
    .join('');

  // Problema → solución
  document.getElementById('problema-titulo').textContent = LANDING.problema.titulo;
  document.getElementById('problema-texto').textContent = LANDING.problema.texto;

  // Beneficios
  document.getElementById('beneficios').innerHTML = LANDING.beneficios.map(b => `
    <div class="beneficio">
      <div class="icono">${b.icono}</div>
      <h3>${b.titulo}</h3>
      <p>${b.texto}</p>
    </div>
  `).join('');

  // Cómo funciona
  document.getElementById('pasos').innerHTML = LANDING.pasos.map(p => `
    <div class="paso">
      <div class="numero">${p.n}</div>
      <h3>${p.titulo}</h3>
      <p>${p.texto}</p>
    </div>
  `).join('');

  // Reseñas
  document.getElementById('resenas').innerHTML = LANDING.resenas.map(r => `
    <div class="resena">
      <div class="resena-estrellas">${estrellas(r.estrellas)}</div>
      <p>“${r.texto}”</p>
      <div class="resena-nombre">${r.nombre}</div>
    </div>
  `).join('');

  // Comparativa
  const comp = LANDING.comparativa;
  document.getElementById('comparativa-titulo').textContent = comp.titulo;
  document.getElementById('comparativa').innerHTML = `
    <tr><th></th><th>Cuenco</th><th class="destacada">AquaMiau</th></tr>
    ${comp.filas.map(([texto, cuenco, fuente]) => `
      <tr>
        <td>${texto}</td>
        <td>${cuenco ? '✅' : '❌'}</td>
        <td class="destacada">${fuente ? '✅' : '❌'}</td>
      </tr>
    `).join('')}`;

  // FAQ (acordeón)
  document.getElementById('faq').innerHTML = LANDING.faq.map(f => `
    <details>
      <summary>${f.p}</summary>
      <p>${f.r}</p>
    </details>
  `).join('');

  // Garantía
  document.getElementById('garantia-titulo').textContent = LANDING.garantia.titulo;
  document.getElementById('garantia-texto').textContent = LANDING.garantia.texto;

  // Barra de compra pegajosa al hacer scroll
  const pegajosa = document.getElementById('barra-pegajosa');
  const packBarato = PRODUCTOS[0];
  pegajosa.querySelector('.precio-pegajoso').textContent = 'Desde ' + precio(packBarato.precio);
  pegajosa.querySelector('button').addEventListener('click', () => {
    agregarAlCarrito(packElegido);
    location.href = 'carrito.html';
  });
  window.addEventListener('scroll', () => {
    pegajosa.classList.toggle('visible', window.scrollY > 600);
  });
}

// ---------- Carrito (carrito.html) ----------

const ENVIO_GRATIS_DESDE = 30;
const COSTE_ENVIO = 3.99;

export function pintarCarrito(contenedor) {
  if (!contenedor.dataset.eventosListos) {
    contenedor.dataset.eventosListos = '1';
    contenedor.addEventListener('click', ev => {
      const d = ev.target.dataset;
      if (d.mas) cambiarCantidad(d.mas, 1);
      else if (d.menos) cambiarCantidad(d.menos, -1);
      else if (d.quitar) quitarDelCarrito(d.quitar);
      else if ('pagar' in d) {
        alert('Demo: aquí iría el pago real con Stripe o PayPal.\n¡Gracias por probar la tienda!');
        return;
      } else return;
      pintarCarrito(contenedor); // repintar tras cualquier cambio
    });
  }

  const carrito = leerCarrito();
  const lineas = Object.entries(carrito)
    .map(([id, cantidad]) => ({ p: PRODUCTOS.find(x => x.id === id), cantidad }))
    .filter(l => l.p);

  if (!lineas.length) {
    contenedor.innerHTML = `
      <div class="vacio">
        <p>Tu carrito está vacío.</p>
        <a class="boton" href="index.html">Volver a la tienda</a>
      </div>`;
    return;
  }

  const subtotal = lineas.reduce((s, l) => s + l.p.precio * l.cantidad, 0);
  const envio = subtotal >= ENVIO_GRATIS_DESDE ? 0 : COSTE_ENVIO;

  contenedor.innerHTML = lineas.map(l => `
    <div class="linea-carrito">
      <a class="mini" href="index.html"><img src="${l.p.imagen}" alt=""></a>
      <div class="info">
        <h3>${l.p.nombre}</h3>
        <div class="unitario">${precio(l.p.precio)} / unidad</div>
      </div>
      <div class="cantidad">
        <button data-menos="${l.p.id}">−</button>
        <span>${l.cantidad}</span>
        <button data-mas="${l.p.id}">+</button>
      </div>
      <strong>${precio(l.p.precio * l.cantidad)}</strong>
      <button class="quitar" data-quitar="${l.p.id}">Quitar</button>
    </div>
  `).join('') + `
    <div class="resumen">
      <div class="fila"><span>Subtotal</span><span>${precio(subtotal)}</span></div>
      <div class="fila"><span>Envío</span><span>${envio ? precio(envio) : 'Gratis'}</span></div>
      <div class="fila total"><span>Total</span><span>${precio(subtotal + envio)}</span></div>
      <button class="boton" style="width:100%;margin-top:14px" data-pagar>Finalizar compra</button>
      <div class="aviso-demo">
        ⚠️ Esto es una demo: el botón de pago no cobra de verdad. Para vender,
        conecta una pasarela real (Stripe, PayPal…) — mira el README de la carpeta <code>tienda/</code>.
      </div>
    </div>`;
}
