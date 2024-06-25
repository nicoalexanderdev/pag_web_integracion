document.addEventListener("DOMContentLoaded", function () {
  const botonContinuar = document.getElementById('continuar-pago');

  // Función para actualizar el costo de envío
  function actualizarCostoEnvio() {
    const radios = document.querySelectorAll('input[name="direccion_envio"]');
    let costoEnvio = 0;
    let direccionSeleccionada = false;
    radios.forEach((radio) => {
      if (radio.checked) {
        direccionSeleccionada = true;
        if (radio.dataid == 7) {
          costoEnvio = 3990;
        }
        else {
            costoEnvio = 5990
        }
      }
    });
    document.getElementById("costo-envio").innerHTML =
      "<small>Costo $" + costoEnvio.toLocaleString() + "</small>";
      botonContinuar.style.display = direccionSeleccionada ? 'block' : 'none';
  }

  // Añadir event listeners a los radio buttons
  document
    .querySelectorAll('input[name="direccion_envio"]')
    .forEach((radio) => {
      radio.addEventListener("change", actualizarCostoEnvio);
    });

  // Llamar a la función una vez para establecer el costo inicial
  actualizarCostoEnvio();

  // Función para calcular y mostrar la fecha de entrega
  function calcularFechaEntrega() {
    const diasParaAgregar = 5;
    const hoy = new Date();
    hoy.setDate(hoy.getDate() + diasParaAgregar);

    const opciones = {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
    };
    const fechaEntregaFormateada = hoy.toLocaleDateString("es-ES", opciones);
    document.getElementById("fecha-entrega").textContent =
      fechaEntregaFormateada.charAt(0).toUpperCase() +
      fechaEntregaFormateada.slice(1);
  }

  // Calcular y mostrar la fecha de entrega
  calcularFechaEntrega();
});
