import pytest
import responses
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.test import Client

# test para crear un direccion
@pytest.mark.django_db
@responses.activate
def test_agregar_direccion_view(client):

    # Crear un usuario de prueba y autenticarlo
    user = User.objects.create_user(
        username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')

    # Datos de ejemplo para la dirección
    direccion_data = {
        'dir': 'Calle Ejemplo',
        'numero': '123',
        'descripcion': 'Descripción de la dirección',
        'comuna': '1'  # ID de la comuna de ejemplo
    }

    # URL de la API simulada
    api_agregar_direccion_url = f'http://{settings.API_BASE_TRANSBANK_URL}/agregar-direccion/'

    # Simular la respuesta de la API
    responses.add(responses.POST, api_agregar_direccion_url, json={
                  'message': 'Dirección agregada correctamente'}, status=201)

    # Hacer una solicitud POST a la vista agregar_direccion
    response = client.post(reverse('agregar_direccion'), data=direccion_data)

    # Verificar que la solicitud fue exitosa
    # Redirección esperada después de agregar la dirección
    assert response.status_code == 302

    # Verificar el comportamiento esperado
    # Redirige al checkout después de agregar la dirección
    assert response.url == reverse('checkout')

    # Verificar que se hizo una solicitud a la API simulada
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == api_agregar_direccion_url
    assert responses.calls[0].request.method == 'POST'
    assert responses.calls[0].request.headers['Content-Type'] == 'application/json'

    # Verificar los datos enviados a la API
    request_data = responses.calls[0].request.body.decode('utf-8')
    assert 'user' in request_data
    assert 'direccion' in request_data
    assert 'num_direccion' in request_data
    assert 'descripcion' in request_data
    assert 'comuna' in request_data

    # Limpiar las respuestas activadas
    responses.reset()



# test para obtener las direcciones del usuario
@pytest.mark.django_db
@responses.activate
def test_checkout_view(client: Client):

    # Crear un usuario de prueba y autenticarlo
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')

    # Datos simulados de direcciones de usuario
    direcciones_usuario = [
        {'id': 1, 'user': user.id ,'direccion': 'Calle Ejemplo', 'num_direccion': 456, 'descripcion': 'Descripción de la dirección', 'comuna': {'id': 1, 'nom_comuna': 'comunaTest', 'provincia': {'id': 1, 'nom_provincia': 'provinciaTest', 'region': {'id': 1, 'nom_region': 'regionTest'}}}},
        {'id': 2, 'user': user.id ,'direccion': 'Av. Principal', 'num_direccion': 123, 'descripcion': 'Otra dirección', 'comuna':{'id': 2, 'nom_comuna': 'comunaTest2', 'provincia': {'id': 2, 'nom_provincia': 'provinciaTest2', 'region': {'id': 2, 'nom_region': 'regionTest2'}}}},
    ]

    # URL de las llamadas a la api de la pagina de checkout
    api_direcciones_url = f'http://{settings.API_BASE_TRANSBANK_URL}/direccion/{user.id}/'
    api_sucursales_url = f'http://{settings.API_BASE_TRANSBANK_URL}/sucursales/'
    api_categorias_url = f'http://{settings.API_BASE_URL}/get-categorias/'
    api_marcas_url = f'http://{settings.API_BASE_URL}/get-marcas/'
    api_dollar_value_url = f'http://{settings.API_BASE_TRANSBANK_URL}/get-dollar-value/'
    api_region_url = f'http://{settings.API_BASE_TRANSBANK_URL}/region/'
    api_provincia_url = f'http://{settings.API_BASE_TRANSBANK_URL}/provincia/'

    # Simular la respuesta de la API 
    responses.add(responses.GET, api_direcciones_url, json=direcciones_usuario, status=200)
    responses.add(responses.GET, api_sucursales_url, json=[], status=200)
    responses.add(responses.GET, api_categorias_url, json=[], status=200)
    responses.add(responses.GET, api_marcas_url, json=[], status=200)
    responses.add(responses.GET, api_dollar_value_url,
                  json={'value': 1.0}, status=200)
    responses.add(responses.GET, api_region_url, json=[], status=200)
    responses.add(responses.GET, api_provincia_url, json=[], status=404)

    # Hacer una solicitud GET a la vista checkout
    response = client.get(reverse('checkout'))

    # Verificar que la solicitud fue exitosa
    assert response.status_code == 200

    # Verificar que se mostraron las direcciones del usuario en la plantilla
    content = response.content.decode()
    for direccion in direcciones_usuario:
        assert direccion['direccion'] in content
        assert str(direccion['num_direccion']) in content
        assert direccion['comuna']['nom_comuna'] in content
        assert direccion['comuna']['provincia']['region']['nom_region'] in content

    # Limpiar las respuestas activadas
    responses.reset()