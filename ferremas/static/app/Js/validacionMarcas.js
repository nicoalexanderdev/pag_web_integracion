$.validator.addMethod("espacios", function (value, element) {
  return value == ' ' || value.trim().length != 0
}, "Espacios no son permitidos");

$.validator.addMethod("lettersOnly", function(value, element) {
  return this.optional(element) || /^[a-zA-Z]+$/.test(value);
}, "Por favor ingresa solo letras");

$(document).ready(function () {
  $('#agregar_marca_form').validate({
      rules: {
          nom_marca:{
              required: true,
              espacios: true,
              lettersOnly: true
          }
      },
      messages: {
          nom_marca: {
              required: "Por favor ingresa nombre de la marca",
              espacios: "No se aceptan espacios",
              lettersOnly: "Solo se aceptan letras"
          }
      }
  });

  event.preventDefault();
})