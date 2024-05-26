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
                minlength: 5,
                maxlength: 10,
                lettersOnly: true
            },
            password: {
                required: true,
                espacios: true,
                minlength: 8,
                maxlength: 8,
            }
        },
        messages: {
            username: {
                required: "Por favor ingresa nombre de usuario",
                espacios: "No se aceptan espacios",
                minlength: "Tu nombre de usuario debe ser de no menos de 5 caracteres",
                maxlength: "Tu nombre de usuario debe ser de no mas de 10 caracteres",
                lettersOnly: "Solo se aceptan letras"
            },
            password: {
                required: "Contraseña es requerido",
                espacios: "No se aceptan espacios",
                minlength: "El minimo debe ser de 8 caracteres",
                maxlength: "El maximo debe der de 8 caracteres"
            }
        }
    })
    event.preventDefault();
})