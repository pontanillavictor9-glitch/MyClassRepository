// Configuración de la tienda monoproducto AquaMiau.
// TODO lo que ve el cliente sale de este archivo: edita aquí textos y precios.

export const TIENDA = {
  nombre: 'AquaMiau',
  eslogan: 'Agua fresca y en movimiento para tu gato, 24/7',
  moneda: '€',
  envio: '📦 Envío GRATIS desde España · Entrega en 3-5 días',
  oferta: '🐱 OFERTA DE LANZAMIENTO: -30% + envío gratis — solo esta semana',
};

// Los "packs" funcionan como productos del carrito: cada uno con su precio.
// precioAntes = precio tachado (el "de antes" de la oferta).
export const PRODUCTOS = [
  {
    id: 'pack-1',
    nombre: 'Fuente AquaMiau 1,5L — 1 unidad',
    precio: 34.99,
    precioAntes: 49.99,
    imagen: 'img/fuente-principal.svg',
    nota: 'Ideal para probar',
  },
  {
    id: 'pack-2',
    nombre: 'Pack 2 fuentes AquaMiau (una por planta)',
    precio: 59.99,
    precioAntes: 99.98,
    imagen: 'img/fuente-principal.svg',
    nota: 'El más vendido — ahorra 10 €',
  },
  {
    id: 'pack-3',
    nombre: 'Pack 3 fuentes AquaMiau (hogar multigato)',
    precio: 79.99,
    precioAntes: 149.97,
    imagen: 'img/fuente-principal.svg',
    nota: 'Máximo ahorro — 25 € menos',
  },
];

export const LANDING = {
  // Galería del héroe (la primera es la principal)
  galeria: [
    'img/fuente-principal.svg',
    'img/gato-bebiendo.svg',
    'img/filtro-capas.svg',
  ],

  // Sello de confianza bajo el botón de compra
  garantias: ['Garantía 30 días', 'Pago 100 % seguro', 'Envío desde España'],

  problema: {
    titulo: '¿Tu gato apenas bebe agua? No es manía: es instinto',
    texto:
      'Los gatos desconfían del agua estancada por naturaleza. Por eso muchos beben ' +
      'menos de lo que necesitan y acaban con deshidratación y problemas renales — ' +
      'el problema de salud nº 1 en gatos. La solución no es insistir: es darle ' +
      'agua como a él le gusta, fresca y en movimiento.',
  },

  beneficios: [
    {
      icono: '💧',
      titulo: 'Agua siempre fresca',
      texto: 'La circulación constante evita el agua estancada y le invita a beber más.',
    },
    {
      icono: '🌿',
      titulo: 'Filtro purificador',
      texto: 'Retiene pelos, restos de comida e impurezas. Agua limpia de verdad.',
    },
    {
      icono: '🔇',
      titulo: 'Súper silenciosa',
      texto: 'No la oirás ni de noche. Tu gato bebe, tú duermes.',
    },
    {
      icono: '🧼',
      titulo: 'Fácil de limpiar',
      texto: 'Se desmonta en segundos y sin herramientas.',
    },
    {
      icono: '🏠',
      titulo: 'Compacta: 1,5 litros',
      texto: 'Agua para 3-4 días sin rellenar y cabe en cualquier rincón.',
    },
    {
      icono: '⚡',
      titulo: 'Bajo consumo',
      texto: 'Enchufada todo el día gasta céntimos al mes.',
    },
  ],

  pasos: [
    { n: '1', titulo: 'Llénala', texto: 'Agua del grifo hasta la marca. 10 segundos.' },
    { n: '2', titulo: 'Enchúfala', texto: 'Empieza a circular y filtrar sola.' },
    { n: '3', titulo: 'Olvídate', texto: 'Rellena cada 3-4 días y cambia el filtro al mes.' },
  ],

  // ⚠️ EJEMPLOS de reseña — sustitúyelas por reseñas REALES de tus clientes
  // en cuanto las tengas. Inventar reseñas es ilegal (y se nota).
  resenas: [
    {
      nombre: 'Laura G. — Madrid',
      estrellas: 5,
      texto:
        'Mi gata ni miraba el cuenco de agua. Con la fuente se pasa el día bebiendo. ' +
        'Ojalá la hubiera comprado antes.',
    },
    {
      nombre: 'Carlos M. — Valencia',
      estrellas: 5,
      texto:
        'Silenciosa de verdad, la tenemos en el salón y no se oye nada. ' +
        'Llegó en 4 días.',
    },
    {
      nombre: 'Ana R. — Sevilla',
      estrellas: 4,
      texto:
        'Muy fácil de limpiar y a mis dos gatos les encanta. Le doy 4 estrellas ' +
        'solo porque me habría gustado que trajera un filtro más de repuesto.',
    },
  ],

  comparativa: {
    titulo: 'Cuenco normal vs AquaMiau',
    filas: [
      ['Agua en movimiento que invita a beber', false, true],
      ['Filtra pelos e impurezas', false, true],
      ['Días sin rellenar', false, true],
      ['Le da igual estar fuera de casa un finde', false, true],
    ],
  },

  faq: [
    {
      p: '¿Cada cuánto hay que cambiar el filtro?',
      r: 'Cada 2-4 semanas según el uso. Es un gesto de 10 segundos y tendrás recambios disponibles en nuestra tienda.',
    },
    {
      p: '¿Hace ruido por la noche?',
      r: 'La bomba es ultra silenciosa (menos de 30 dB, más bajo que un susurro). Solo oirás un leve murmullo de agua si estás al lado.',
    },
    {
      p: '¿Sirve para perros pequeños?',
      r: 'Sí, para perros mini y pequeños también. Para perros medianos o grandes recomendamos rellenarla más a menudo por su capacidad de 1,5 L.',
    },
    {
      p: '¿Cuánto tarda el envío?',
      r: 'Enviamos desde España: 3-5 días laborables con seguimiento incluido.',
    },
    {
      p: '¿Y si a mi gato no le gusta?',
      r: 'Tienes 30 días de garantía: si no os convence, te devolvemos el dinero. Sin preguntas raras.',
    },
  ],

  garantia: {
    titulo: 'Garantía "Ronroneo o Reembolso" de 30 días',
    texto:
      'Pruébala 30 días. Si tu gato no bebe más agua que antes, escríbenos y te ' +
      'devolvemos hasta el último céntimo. El riesgo lo asumimos nosotros.',
  },
};
