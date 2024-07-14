$.validator.addMethod(
  "espacios",
  function (value, element) {
    return value == " " || value.trim().length != 0;
  },
  "Espacios no son permitidos"
);

$.validator.addMethod(
  "lettersOnly",
  function (value, element) {
    return this.optional(element) || /^[a-zA-Z]+$/.test(value);
  },
  "Por favor ingresa solo letras"
);

$(document).ready(function () {
  $("#agregar_producto_form").validate({
    rules: {
      nombre: {
        required: true,
        espacios: true,
        lettersOnly: true,
      },
      precio: {
        required: true,
      },
      stock: {
        required: true,
      },
      categoria: {
        required: true,
      },
      marca: {
        required: true,
      },
    },
    messages: {
      nombre: {
        required: "Por favor ingresa nombre del producto",
        espacios: "No se aceptan espacios",
        lettersOnly: "Solo se aceptan letras",
      },
      precio: {
        required: "precio es reuqerido",
      },
      stock: {
        required: "stock es requerido",
      },
      categoria: {
        required: "categoria es requerido",
      },
      marca: {
        required: "marca es requerido",
      },
    },
  });

  event.preventDefault();
});
