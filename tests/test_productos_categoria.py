import pytest
import responses
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings

@pytest.mark.django_db
@responses.activate
def test_categoria_view(client):
    # Datos simulados de respuesta de la API
    categoria_id = 1
    productos_categoria = {
        'categoria': {'id': 1, 'nom_categoria': 'categoria 1'},
        'productos': [
            {'id': 1, 'nombre': 'Martillo', 'precio': 500, 'marca': {'id': 1, 'nom_marca': 'marcaTest'}, 'categoria': {'id': categoria_id, 'nom_categoria': 'categoria 1'}},
            {'id': 2, 'nombre': 'pala', 'precio': 800, 'marca': {'id': 1, 'nom_marca': 'marcaTest'}, 'categoria': {'id': categoria_id, 'nom_categoria': 'categoria 1'}},
        ]
    }

    # URL de la API simulada para obtener productos de una categoría
    api_productos_categoria_url = f'http://{settings.API_BASE_URL}/get-productos-categoria/{categoria_id}/'

    # Simular respuesta exitosa de la API
    responses.add(responses.GET, api_productos_categoria_url, json=productos_categoria, status=200)

    # Hacer una solicitud GET a la vista categoria
    response = client.get(reverse('categoria', kwargs={'id': categoria_id}))

    # Verificar que la solicitud fue exitosa
    assert response.status_code == 200

    # Verificar que se mostraron los productos de la categoría en la plantilla
    content = response.content.decode()
    assert productos_categoria['categoria']['nom_categoria'] in content
    for producto in productos_categoria['productos']:
        assert producto['nombre'] in content
        assert str(producto['precio']) in content
        assert producto['marca']['nom_marca'] in content

    # Limpiar las respuestas activadas
    responses.reset()

@pytest.mark.django_db
@responses.activate
def test_categoria_view_error(client):
    # Datos simulados de respuesta de la API
    categoria_id = 1

    # URL de la API simulada para obtener productos de una categoría
    api_productos_categoria_url = f'http://{settings.API_BASE_URL}/get-productos-categoria/{categoria_id}/'

    # Simular respuesta de error de la API (por ejemplo, 404 Not Found)
    responses.add(responses.GET, api_productos_categoria_url, status=404)

    # Hacer una solicitud GET a la vista categoria
    response = client.get(reverse('categoria', kwargs={'id': categoria_id}))

    # Verificar que la vista redirige a 'home' cuando hay un error en la API
    assert response.status_code == 302
    assert response.url == reverse('home')

    # Limpiar las respuestas activadas
    responses.reset()
