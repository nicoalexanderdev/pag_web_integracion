//metodo creado para evitar los espacios en los inputs
$.validator.addMethod("espacios", function (value, element) {
    return value == ' ' || value.trim().length != 0
}, "Espacios no son permitidos");

$.validator.addMethod("lettersOnly", function(value, element) {
    return this.optional(element) || /^[a-zA-Z]+$/.test(value);
}, "Por favor ingresa solo letras");

$(document).ready(function () {
    $('#formularioRegistro').validate({
        rules: {
            username: {
                required: true,
                espacios: true,
                lettersOnly: true
            },
            first_name: {
                required: true,
                espacios: true,
                minlength: 3,
                maxlength: 30,
                lettersOnly: true
            },
            last_name: {
                required: true,
                espacios: true,
                minlength: 3,
                maxlength: 30,
                lettersOnly: true
            },
            email: {
                required: true,
                espacios: true,
                email: true
            },
            password1: {
                required: true,
                espacios: true,
            },
            password2: {
                required: true,
                espacios: true,
                equalTo: "#id_password1"
             }
        },
        messages: {
            username: {
                required: "Por favor ingresa nombre de usuario",
                espacios: "No se aceptan espacios",
                lettersOnly: "Solo se aceptan letras"
            },
            first_name: {
                required: "Tu nombre es requerido",
                espacios: "No se aceptan espacios",
                minlength: "Tu nombre debe ser de no menos de 3 caracteres",
                maxlength: "Tu nombre debe ser de no mas de 30 caracteres",
                lettersOnly: "Solo se aceptan letras"
            },
            last_name: {
                required: "Tu apellido es requerido",
                espacios: "No se aceptan espacios",
                minlength: "Tu apellido debe ser de no menos de 3 caracteres",
                maxlength: "Tu apellido debe ser de no mas de 30 caracteres",
                lettersOnly: "Solo se aceptan letras"
            },
            email: {
                required: "Tu correo es requerido",
                espacios: "No se aceptan espacios",
                email: "Ingresa un correo válido"
            },
            password1: {
                required: "Contraseña es requerido",
                espacios: "No se aceptan espacios",
            },
            password2: {
                required: "Contraseña es requerido",
                espacios: "No se aceptan espacios",
                equalTo: "Debe ingresar la misma contraseña"
            }
        }
    })
    event.preventDefault();
})