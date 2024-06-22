
const inputDireccion = document.getElementById('direccion');
const inputNumero = document.getElementById('numero');

// Función para buscar dirección y autocompletar otros campos
function buscarDireccion() {
  const direccionCompleta = inputDireccion.value.trim(); // Obtener el valor del input y eliminar espacios en blanco
  autocompletarDireccionCompleta(direccionCompleta);
}
const input = document.getElementById('direccion');

let map;
let marker;
let autocomplete;

function initAutoComplete() {
  autocomplete = new google.maps.places.Autocomplete(input);
  autocomplete.addListener('place_changed', function () {
    const place = autocomplete.getPlace();
    map.setCenter(place.geometry.location);
    marker.setPosition(place.geometry.location);
  })
}

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: -33.4332521, lng: -70.6156447 },
    zoom: 17,
  });
  marker = new google.maps.Marker({
    position: { lat: -33.4332521, lng: -70.6156447 },
    map: map,
  });
  initAutoComplete();
}

// Función para autocompletar otros inputs basados en la dirección completa proporcionada
async function autocompletarDireccionCompleta(direccionCompleta) {
  const inputDireccion = document.getElementById('dir');
  const inputNumero = document.getElementById('numero');

  // Crear una instancia de AutocompleteService
  const autocompleteService = new google.maps.places.AutocompleteService();

  // Realizar solicitud al servicio de autocompletado con la dirección completa
  autocompleteService.getPlacePredictions({ input: direccionCompleta }, (predictions, status) => {
    if (status === google.maps.places.PlacesServiceStatus.OK && predictions && predictions.length > 0) {
      const placeId = predictions[0].place_id;

      // Crear una instancia de PlacesService para obtener detalles del lugar
      const placesService = new google.maps.places.PlacesService(document.createElement('div'));
      placesService.getDetails({ placeId }, (place, status) => {
        if (status === google.maps.places.PlacesServiceStatus.OK && place) {
          // Extraer componentes de la dirección
          const addressComponents = place.address_components;
          let streetNumber = '';
          let route = '';

          // Buscar el componente de número de calle y nombre de calle
          for (const component of addressComponents) {
            const types = component.types;

            if (types.includes('street_number')) {
              streetNumber = component.short_name;
            }

            if (types.includes('route')) {
              route = component.short_name;
            }

            // Salir del bucle si ya se han encontrado ambos componentes
            if (streetNumber && route) {
              break;
            }
          }

          // Autocompletar los inputs correspondientes
          inputDireccion.value = route; // Autocompletar el input de dirección (por ejemplo, "Cartagena")
          inputNumero.value = streetNumber; // Autocompletar el input de número de dirección (por ejemplo, "2243")
        } else {
          console.error('Error al obtener detalles del lugar:', status);
        }
      });
    } else {
      console.error('Error al obtener predicciones de autocompletado:', status);
    }
  });
}

