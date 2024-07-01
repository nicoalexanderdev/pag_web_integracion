import pytest
import responses
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings

@pytest.mark.django_db
@responses.activate
def test_marca_view(client):
    # Datos simulados de respuesta de la API
    marca_id = 1
    productos_marca = {
        'marca': {'id': 1, 'nom_marca': 'marcaTest'},
        'productos': [
            {'id': 1, 'nombre': 'Martillo', 'precio': 500, 'marca': {'id': marca_id, 'nom_marca': 'marcaTest'}, 'categoria': {'id': 2, 'nom_categoria': 'categoria 1'}},
            {'id': 2, 'nombre': 'pala', 'precio': 800, 'marca': {'id': marca_id, 'nom_marca': 'marcaTest'}, 'categoria': {'id': 2, 'nom_categoria': 'categoria 1'}},
        ]
    }

    # URL de la API simulada para obtener productos de una marca
    api_productos_marca_url = f'http://{settings.API_BASE_URL}/get-productos-marca/{marca_id}/'

    # Simular respuesta exitosa de la API
    responses.add(responses.GET, api_productos_marca_url, json=productos_marca, status=200)

    # Hacer una solicitud GET a la vista marca
    response = client.get(reverse('marca', kwargs={'id': marca_id}))

    # Verificar que la solicitud fue exitosa
    assert response.status_code == 200

    # Verificar que se mostraron los productos de la marca en la plantilla
    content = response.content.decode()
    assert productos_marca['marca']['nom_marca'] in content
    for producto in productos_marca['productos']:
        assert producto['nombre'] in content
        assert str(producto['precio']) in content

    # Limpiar las respuestas activadas
    responses.reset()

@pytest.mark.django_db
@responses.activate
def test_marca_view_error(client):
    # Datos simulados de respuesta de la API
    marca_id = 1

    # URL de la API simulada para obtener productos de una marca
    api_productos_marca_url = f'http://{settings.API_BASE_URL}/get-productos-marca/{marca_id}/'

    # Simular respuesta de error de la API (por ejemplo, 500 Internal Server Error)
    responses.add(responses.GET, api_productos_marca_url, status=500)

    # Hacer una solicitud GET a la vista marca
    response = client.get(reverse('marca', kwargs={'id': marca_id}))

    # Verificar que la vista redirige a 'home' cuando hay un error en la API
    assert response.status_code == 302
    assert response.url == reverse('home')

    # Limpiar las respuestas activadas
    responses.reset()
