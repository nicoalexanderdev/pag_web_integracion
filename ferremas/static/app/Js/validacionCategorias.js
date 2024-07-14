$.validator.addMethod("espacios", function (value, element) {
  return value == ' ' || value.trim().length != 0
}, "Espacios no son permitidos");

$.validator.addMethod("lettersOnly", function(value, element) {
  return this.optional(element) || /^[a-zA-Z]+$/.test(value);
}, "Por favor ingresa solo letras");

$(document).ready(function () {
  $('#agregar_categoria_form').validate({
      rules: {
          nom_categoria:{
              required: true,
              espacios: true,
              lettersOnly: true
          }
      },
      messages: {
        nom_categoria: {
              required: "Por favor ingresa nombre de la categoria",
              espacios: "No se aceptan espacios",
              lettersOnly: "Solo se aceptan letras"
          }
      }
  });

  event.preventDefault();
})