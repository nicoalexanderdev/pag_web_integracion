$(document).ready(function () {
  $('#ir-a-pagar-form').validate({
      rules: {
        tipo_documento: {
          required: true
        },
        forma_pago: {
          required: true
        }
      },
      messages: {
          tipo_documento: {
            required: "Por favor selecciona tipo de documento"
          },
          forma_pago: {
            required: "Por favor selecciona metodo de pago"
          }
      }
  });

  event.preventDefault();
})