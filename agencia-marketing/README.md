# Impulsa Digital — Sitio web de agencia de marketing

Página web de una agencia de marketing ficticia, construida con HTML, CSS y JavaScript puros (sin frameworks ni dependencias).

## Cómo verla

Abre el archivo `index.html` en tu navegador, o si tienes Python instalado:

```bash
cd agencia-marketing
python -m http.server 8000
```

y visita http://localhost:8000

## Estructura

| Archivo      | Qué contiene                                                    |
|--------------|-----------------------------------------------------------------|
| `index.html` | La estructura de la página: navegación, hero, servicios, portafolio, equipo y contacto |
| `styles.css` | Todos los estilos: colores, tarjetas, diseño responsive          |
| `script.js`  | Interactividad: menú hamburguesa y confirmación del formulario   |

## Secciones de la página

1. **Inicio (hero):** mensaje principal con botones de llamada a la acción
2. **Servicios:** tarjetas con los servicios de la agencia
3. **Portafolio:** galería de proyectos de ejemplo
4. **Equipo:** integrantes de la agencia
5. **Contacto:** formulario (muestra confirmación sin enviar datos a un servidor)

## Ideas para seguir mejorando

- Conectar el formulario a un servicio real (por ejemplo Formspree o un backend propio)
- Reemplazar los proyectos del portafolio con imágenes reales
- Publicar el sitio gratis con GitHub Pages (Settings → Pages)
