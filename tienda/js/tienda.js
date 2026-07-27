// Lógica común de la tienda: pintar catálogo, ficha de producto y carrito.
// El carrito se guarda en localStorage, así sobrevive a recargas de página.

import { PRODUCTOS, TIENDA } from './productos.js';

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

export function vaciarCarrito() {
  guardarCarrito({});
}

function unidadesTotales() {
  return Object.values(leerCarrito()).reduce((suma, n) => suma + n, 0);
}

export function precio(n) {
  return n.toFixed(2).replace('.', ',') + ' ' + TIENDA.moneda;
}

// ---------- Elementos comunes (cabecera, contador, pie) ----------

export function pintarContador() {
  const el = document.querySelector('.contador-carrito');
  if (el) el.textContent = unidadesTotales();
}

export function iniciarPagina() {
  document.querySelectorAll('[data-tienda-nombre]').forEach(el => {
    el.innerHTML = TIENDA.nombre.replace(/(\S+)$/, '<span>$1</span>');
  });
  const barra = document.querySelector('.barra-envio');
  if (barra) barra.textContent = TIENDA.envio;
  pintarContador();
}

// ---------- Catálogo (index.html) ----------

export function pintarCatalogo(contenedor) {
  contenedor.innerHTML = PRODUCTOS.map(p => `
    <article class="tarjeta">
      <a class="imagen" href="producto.html?id=${p.id}">
        ${p.etiqueta ? `<span class="etiqueta">${p.etiqueta}</span>` : ''}
        <img src="${p.imagen}" alt="${p.nombre}">
      </a>
      <div class="cuerpo">
        <h3><a href="producto.html?id=${p.id}">${p.nombre}</a></h3>
        <div class="precio">${precio(p.precio)}</div>
        <button class="boton" data-agregar="${p.id}">Añadir al carrito</button>
      </div>
    </article>
  `).join('');

  contenedor.addEventListener('click', ev => {
    const id = ev.target.dataset.agregar;
    if (!id) return;
    agregarAlCarrito(id);
    ev.target.textContent = '✓ Añadido';
    setTimeout(() => { ev.target.textContent = 'Añadir al carrito'; }, 1200);
  });
}

// ---------- Ficha (producto.html) ----------

export function pintarFicha(contenedor) {
  const id = new URLSearchParams(location.search).get('id');
  const p = PRODUCTOS.find(x => x.id === id);

  if (!p) {
    contenedor.innerHTML = `
      <div class="vacio">
        <p>Producto no encontrado.</p>
        <a class="boton" href="index.html">Volver a la tienda</a>
      </div>`;
    return;
  }

  document.title = `${p.nombre} — ${TIENDA.nombre}`;
  contenedor.innerHTML = `
    <div class="imagen"><img src="${p.imagen}" alt="${p.nombre}"></div>
    <div>
      ${p.etiqueta ? `<span class="etiqueta" style="position:static">${p.etiqueta}</span>` : ''}
      <h1>${p.nombre}</h1>
      <div class="precio">${precio(p.precio)}</div>
      <p class="descripcion">${p.descripcion}</p>
      <ul class="ventajas">
        <li>${TIENDA.envio}</li>
        <li>Devolución gratuita en 30 días</li>
        <li>Pago 100 % seguro</li>
      </ul>
      <button class="boton" data-agregar>Añadir al carrito</button>
      <a class="boton secundario" href="carrito.html" style="margin-left:8px">Ver carrito</a>
    </div>`;

  contenedor.querySelector('[data-agregar]').addEventListener('click', ev => {
    agregarAlCarrito(p.id);
    ev.target.textContent = '✓ Añadido';
    setTimeout(() => { ev.target.textContent = 'Añadir al carrito'; }, 1200);
  });
}

// ---------- Carrito (carrito.html) ----------

const ENVIO_GRATIS_DESDE = 40;
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
        <a class="boton" href="index.html">Ver productos</a>
      </div>`;
    return;
  }

  const subtotal = lineas.reduce((s, l) => s + l.p.precio * l.cantidad, 0);
  const envio = subtotal >= ENVIO_GRATIS_DESDE ? 0 : COSTE_ENVIO;

  contenedor.innerHTML = lineas.map(l => `
    <div class="linea-carrito">
      <a class="mini" href="producto.html?id=${l.p.id}"><img src="${l.p.imagen}" alt=""></a>
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
