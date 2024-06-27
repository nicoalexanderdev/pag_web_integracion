$(document).ready(function () {
  $('#ir-a-pagar-form').validate({
      rules: {
        tipo_documento: {
          required: true
        },
        transbank: {
          required: true
        }
      },
      messages: {
          tipo_documento: {
            required: "Por favor selecciona tipo de documento"
          },
          transbank: {
            required: "Por favor selecciona metodo de pago"
          }
      }
  });

  event.preventDefault();
})