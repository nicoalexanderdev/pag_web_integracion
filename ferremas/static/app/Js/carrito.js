function continuar() {
    // Obtener el valor seleccionado del radio button
    var opcionSeleccionada = document.querySelector('input[name="listGroupRadio"]:checked').value;

    // Mostrar u ocultar los formularios según la opción seleccionada
    if (opcionSeleccionada === "retiro") {
      document.getElementById('formulario-retiro').style.display = 'block';
      document.getElementById('formulario-despacho').style.display = 'none';
    } else if (opcionSeleccionada === "despacho") {
      document.getElementById('formulario-retiro').style.display = 'none';
      document.getElementById('formulario-despacho').style.display = 'block';
    }
    // Actualizar la barra de progreso al 75%
    document.getElementById('barra-progreso').style.width = '70%';
    document.getElementById('barra-progreso').setAttribute('aria-valuenow', '70');
}