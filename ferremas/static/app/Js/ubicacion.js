
// // Variables globales para almacenar datos
// let regiones = [];
// let provincias = [];
// let comunas = [];

// // Elementos del formulario
// let selectRegiones = document.getElementById('regiones');
// let selectProvincias = document.getElementById('provincias');
// let selectComunas = document.getElementById('comunas');

// // Función para cargar las regiones desde la API
// async function cargarRegiones() {
// 	try {
// 			const response = await fetch('http://127.0.0.1:8000/api/compras/region');
// 			if (!response.ok) {
// 					throw new Error('No se pudo cargar las regiones');
// 			}
// 			const data = await response.json();
// 			regiones = data.regiones; // Suponiendo que la API devuelve un objeto con un array de regiones
// 			llenarSelectRegiones();
// 	} catch (error) {
// 			console.error('Error al cargar regiones:', error.message);
// 	}
// }

// // Función para llenar el select de regiones
// function llenarSelectRegiones() {
// 	regiones.forEach((region, index) => {
// 			let option = document.createElement('option');
// 			option.textContent = region.NombreRegion;
// 			option.value = index;
// 			selectRegiones.appendChild(option);
// 	});
// }