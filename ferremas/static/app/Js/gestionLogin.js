$.validator.addMethod("espacios", function (value, element) {
    return value == ' ' || value.trim().length != 0
}, "Espacios no son permitidos");

$.validator.addMethod("lettersOnly", function(value, element) {
    return this.optional(element) || /^[a-zA-Z]+$/.test(value);
}, "Por favor ingresa solo letras");

$(document).ready(function () {
    $('#formularioLogin').validate({
        rules: {
            username:{
                required: true,
                espacios: true,
                lettersOnly: true
            },
            password: {
                required: true,
                espacios: true,
            }
        },
        messages: {
            username: {
                required: "Por favor ingresa nombre de usuario",
                espacios: "No se aceptan espacios",
                lettersOnly: "Solo se aceptan letras"
            },
            password: {
                required: "Contraseña es requerido",
                espacios: "No se aceptan espacios",
            }
        }
    });

    event.preventDefault();
})