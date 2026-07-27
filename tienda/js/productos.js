// Catálogo de la tienda. Edita este archivo para poner TUS productos.
//
// Campos:
//   id             — identificador único (se usa en la URL de la ficha)
//   nombre         — nombre que ve el cliente
//   precio         — precio de venta al público (lo que cobras tú)
//   costeProveedor — lo que te cuesta en el proveedor (AliExpress, CJ, etc.)
//                    Solo lo usas tú para calcular margen; NO se muestra al cliente.
//   proveedorUrl   — enlace al producto en tu proveedor (para pedirlo cuando vendas)
//   imagen         — ruta de la imagen (pon fotos reales del proveedor al lanzar)
//   descripcion    — texto de venta de la ficha
//   etiqueta       — opcional: "Más vendido", "Oferta", "Nuevo"...

export const TIENDA = {
  nombre: 'Nova Desk',
  eslogan: 'Accesorios que mejoran tu escritorio',
  moneda: '€',
  envio: 'Envío gratis a partir de 40 €',
};

export const PRODUCTOS = [
  {
    id: 'lampara-led',
    nombre: 'Lámpara LED de escritorio con carga inalámbrica',
    precio: 34.99,
    costeProveedor: 12.4,
    proveedorUrl: '',
    imagen: 'img/lampara-led.svg',
    etiqueta: 'Más vendido',
    descripcion:
      'Lámpara regulable en 3 tonos de luz con base de carga inalámbrica para tu móvil. ' +
      'Brazo plegable, puerto USB extra y consumo mínimo. Ideal para estudiar o teletrabajar.',
  },
  {
    id: 'soporte-portatil',
    nombre: 'Soporte ergonómico de aluminio para portátil',
    precio: 27.99,
    costeProveedor: 9.8,
    proveedorUrl: '',
    imagen: 'img/soporte-portatil.svg',
    etiqueta: 'Nuevo',
    descripcion:
      'Eleva la pantalla a la altura de tus ojos y despídete del dolor de cuello. ' +
      'Aluminio ligero, plegable y compatible con portátiles de 10" a 17".',
  },
  {
    id: 'teclado-mecanico',
    nombre: 'Teclado mecánico compacto RGB',
    precio: 49.99,
    costeProveedor: 21.5,
    proveedorUrl: '',
    imagen: 'img/teclado-mecanico.svg',
    etiqueta: '',
    descripcion:
      'Formato 65% con switches rojos silenciosos, retroiluminación RGB personalizable ' +
      'y conexión USB-C. Perfecto para gaming y oficina.',
  },
  {
    id: 'organizador-cables',
    nombre: 'Organizador magnético de cables (pack 6)',
    precio: 12.99,
    costeProveedor: 3.2,
    proveedorUrl: '',
    imagen: 'img/organizador-cables.svg',
    etiqueta: 'Oferta',
    descripcion:
      'Clips magnéticos autoadhesivos que mantienen tus cables siempre a mano. ' +
      'Se acabó buscar el cargador detrás de la mesa.',
  },
  {
    id: 'alfombrilla-xl',
    nombre: 'Alfombrilla XL antideslizante 80×30 cm',
    precio: 18.99,
    costeProveedor: 6.1,
    proveedorUrl: '',
    imagen: 'img/alfombrilla-xl.svg',
    etiqueta: '',
    descripcion:
      'Superficie de microtejido de deslizamiento rápido, base de goma antideslizante ' +
      'y bordes cosidos. Cubre teclado y ratón de una vez.',
  },
  {
    id: 'hub-usb',
    nombre: 'Hub USB-C 7 en 1 con HDMI 4K',
    precio: 29.99,
    costeProveedor: 11.9,
    proveedorUrl: '',
    imagen: 'img/hub-usb.svg',
    etiqueta: '',
    descripcion:
      'HDMI 4K, 2× USB 3.0, lector SD/microSD y carga PD de 100 W en un solo accesorio ' +
      'de bolsillo. Convierte tu portátil en una estación de trabajo.',
  },
];
