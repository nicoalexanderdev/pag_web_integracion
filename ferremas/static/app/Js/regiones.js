let regionesSelect = document.getElementById('regiones');
let provinciasSelect = document.getElementById('provincias');
let comunasSelect = document.getElementById('comunas');

// Función para cargar provincias y comunas basadas en la selección actual
function cargarProvinciasYComunas() {
    let regionId = regionesSelect.value;

    fetch(`http://localhost:8000/api/compras/provincia/${regionId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Limpiar opciones anteriores de provincias
            provinciasSelect.innerHTML = '';

            // Agregar nuevas opciones de provincias
            data.forEach(provincia => {
                let option = document.createElement('option');
                option.value = provincia.id;
                option.textContent = provincia.nom_provincia;
                provinciasSelect.appendChild(option);
            });

            // Si hay provincias cargadas, cargar las comunas de la primera provincia
            if (data.length > 0) {
                cargarComunas(data[0].id);  // Cargar comunas de la primera provincia
            }
        })
        .catch(error => {
            console.error('Error fetching provincias:', error);
        });
}

// Función para cargar las comunas de una provincia seleccionada
function cargarComunas(provinciaId) {
    fetch(`http://localhost:8000/api/compras/comuna/${provinciaId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Limpiar opciones anteriores de comunas
            comunasSelect.innerHTML = '';

            // Agregar nuevas opciones de comunas
            data.forEach(comuna => {
                let option = document.createElement('option');
                option.value = comuna.id;
                option.textContent = comuna.nom_comuna;
                comunasSelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error fetching comunas:', error);
        });
}

// Cargar provincias y comunas al cargar la página inicialmente
cargarProvinciasYComunas();

// Escuchar el evento change en el select de regiones
regionesSelect.addEventListener('change', cargarProvinciasYComunas);

// Escuchar el evento change en el select de provincias
provinciasSelect.addEventListener('change', function() {
    let provinciaId = this.value;
    cargarComunas(provinciaId);
});