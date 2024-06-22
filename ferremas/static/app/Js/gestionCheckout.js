$.validator.addMethod("espacios", function (value, element) {
    return value == ' ' || value.trim().length != 0
}, "Espacios no son permitidos");

$.validator.addMethod("lettersOnly", function(value, element) {
    return this.optional(element) || /^[a-zA-Z]+$/.test(value);
}, "Por favor ingresa solo letras");

$(document).ready(function () {
    $('#despacho-form').validate({
        rules: {
            buscarDireccion: {
                required: true
            },
            dir:{
                required: true,
                espacios: true,
                lettersOnly: true
            },
            numero: {
                required: true,
                espacios: true,
                number: true
            },
            descripcion: {
                number: true
            },
            region: {
                required: true
            },
            comuna: {
                required: true
            }
        },
        messages: {
            buscarDireccion: {
                required:"Por favor busca tu direccion"
            },
            dir: {
                required: "Por favor busca tu direccion",
                espacios: "No se aceptan espacios",
                lettersOnly: "Solo se aceptan letras"
            },
            numero: {
                required: "Por favor ingresa tu numero de direccion",
                espacios: "No se aceptan espacios",
                number: "Solo se aceptan numeros"
            },
            descripcion: {
                number: "Solo se aceptan numeros en este campo"
            },
            region: {
                required: "Region es requerida"
            },
            comuna: {
                required: "Comuna es requerida"
            }
        }
    });

    event.preventDefault();
})