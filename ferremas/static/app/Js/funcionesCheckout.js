document.addEventListener("DOMContentLoaded", function () {
  const botonContinuar = document.getElementById("continuar-pago");
  const radioDirecciones = document.querySelectorAll('input[name="direcciones_usuario"]');
  const radioTipoEntrega = document.querySelectorAll('input[name="radios_tipo_entrega"]');
  const radioSucursal = document.querySelectorAll('input[name="sucursal"]');
  const costoEnvioElemento = document.getElementById("costo-envio");

  function actualizarCostoEnvio() {
    let costoEnvio = 0;
    let direccionSeleccionada = false;

    radioDirecciones.forEach(function (radio) {
      if (radio.checked) {
        direccionSeleccionada = true;
        const dataid = radio.getAttribute("data-id");

        console.log(`Radio seleccionado: ${radio.value}, data-id: ${dataid}`);

        if (dataid === "7") {
          costoEnvio = 3990;
        } else {
          costoEnvio = 5990;
        }

        console.log(`Costo de envío calculado: ${costoEnvio}`);
        costoEnvioElemento.innerHTML = "Costo $" + costoEnvio.toLocaleString();
        botonContinuar.style.display = direccionSeleccionada ? "block" : "none";
      }
    });
  }

  function manejarCambioTipoEntrega() {
    const tipoEntrega = this.value;

    document.querySelector('input[name="tipo_entrega"]').value = tipoEntrega;

    if (tipoEntrega === "Retiro") {
      document.getElementById('formulario-retiro').style.display = 'block';
      document.getElementById('formulario-despacho').style.display = 'none';
      document.getElementById('barra-progreso').style.width = '70%';
      document.getElementById('barra-progreso').setAttribute('aria-valuenow', '70');

      radioSucursal.forEach(function (radio) {
        radio.addEventListener("change", function () {
          const sucursal = this.value;
          document.getElementById("direccion-form").value = sucursal;
          botonContinuar.style.display = sucursal ? "block" : "none";
        });
      });

    } else if (tipoEntrega === "Despacho") {
      document.getElementById('formulario-retiro').style.display = 'none';
      document.getElementById('formulario-despacho').style.display = 'block';
      document.getElementById('barra-progreso').style.width = '70%';
      document.getElementById('barra-progreso').setAttribute('aria-valuenow', '70');

      radioDirecciones.forEach(function (radio) {
        radio.addEventListener("change", function () {
          const direccion = this.value;
          const regionId = this.getAttribute("data-id");

          document.getElementById("direccion-form").value = direccion;
          document.getElementById("region-id").value = regionId;

          actualizarCostoEnvio();
        });
      });

      actualizarCostoEnvio();
    }
  }

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

  radioTipoEntrega.forEach(function (radio) {
    radio.addEventListener("change", manejarCambioTipoEntrega);
  });

  radioDirecciones.forEach(function (radio) {
    radio.addEventListener('change', function () {
      const direccion = this.value;
      const regionId = this.getAttribute('data-id');

      document.getElementById('direccion-form').value = direccion;
      document.getElementById('region-id').value = regionId;
    });
  });

  calcularFechaEntrega();
});
