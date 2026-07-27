// Menú hamburguesa para pantallas pequeñas
const botonMenu = document.getElementById("botonMenu");
const menu = document.getElementById("menu");

botonMenu.addEventListener("click", () => {
  menu.classList.toggle("abierto");
});

// Cerrar el menú al hacer clic en un enlace
menu.querySelectorAll("a").forEach((enlace) => {
  enlace.addEventListener("click", () => menu.classList.remove("abierto"));
});

// Formulario de contacto: muestra una confirmación sin recargar la página.
// (En un proyecto real aquí se enviarían los datos a un servidor.)
const formulario = document.getElementById("formularioContacto");
const confirmacion = document.getElementById("confirmacion");

formulario.addEventListener("submit", (evento) => {
  evento.preventDefault();
  confirmacion.hidden = false;
  formulario.reset();
  setTimeout(() => {
    confirmacion.hidden = true;
  }, 5000);
});
