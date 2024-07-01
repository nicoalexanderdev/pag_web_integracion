import pytest
import responses
from django.urls import reverse
from django.conf import settings
from django.test import Client

# test para traer y desplegar correctamente en la pagina todos los productos
@pytest.mark.django_db
@responses.activate
def test_index_view(client):

    productos_mock = [
        {
            'id': 1,
            'nombre': 'Producto 1',
            'precio': 100,
            'descripcion': 'Descripción del Producto 1',
            'image_url': 'http://example.com/image1.jpg',
            'stock': 10,
            'marca': {'id': 1, 'nom_marca': 'Marca 1'},
            'categoria': {'id': 1, 'nom_categoria': 'Categoría 1'}
        },
        {
            'id': 2,
            'nombre': 'Producto 2',
            'precio': 200,
            'descripcion': 'Descripción del Producto 2',
            'image_url': 'http://example.com/image2.jpg',
            'stock': 20,
            'marca': {'id': 2, 'nom_marca': 'Marca 2'},
            'categoria': {'id': 2, 'nom_categoria': 'Categoría 2'}
        }
    ]

    # URLs de la API
    api_productos_url = f'http://{settings.API_BASE_URL}/'
    api_categorias_url = f'http://{settings.API_BASE_URL}/get-categorias/'
    api_marcas_url = f'http://{settings.API_BASE_URL}/get-marcas/'
    api_dollar_value_url = f'http://{settings.API_BASE_TRANSBANK_URL}/get-dollar-value/'
    api_region_url = f'http://{settings.API_BASE_TRANSBANK_URL}/region/'

    # Simular las respuestas de la API
    responses.add(responses.GET, api_productos_url,
                  json=productos_mock, status=200)
    responses.add(responses.GET, api_categorias_url, json=[], status=200)
    responses.add(responses.GET, api_marcas_url, json=[], status=200)
    responses.add(responses.GET, api_dollar_value_url,
                  json={'value': 1.0}, status=200)
    responses.add(responses.GET, api_region_url, json=[], status=200)

    # Hacer una solicitud GET a la vista index
    response = client.get(reverse('home'))

    # Verificar que la solicitud fue exitosa
    assert response.status_code == 200

    # Verificar que los productos se renderizan correctamente en la plantilla
    content = response.content.decode()
    for producto in productos_mock:
        assert producto['nombre'] in content
        assert str(producto['precio']) in content
        assert producto['marca']['nom_marca'] in content



# test para trer y desplegar un producto especifico
@pytest.mark.django_db
@responses.activate
def test_descripcion_producto_view(client: Client):

    producto = {
        'id': 1,
        'nombre': 'Producto 1',
        'precio': 100,
        'descripcion': 'Descripción del Producto 1',
        'image_url': 'http://example.com/image1.jpg',
        'stock': 10,
        'marca': {'id': 1, 'nom_marca': 'Marca 1'},
        'categoria': {'id': 1, 'nom_categoria': 'Categoría 1'}
    }

    # URL de la API para obtener el producto con id=1
    api_producto_url = f'http://{settings.API_BASE_URL}/get-producto/1/'

    # Simular la respuesta de la API
    responses.add(responses.GET, api_producto_url, json=producto, status=200)

    # Hacer una solicitud GET a la vista detalle_producto
    response = client.get(reverse('detalle_producto', kwargs={'id': 1}))

    # Verificar que la solicitud fue exitosa
    assert response.status_code == 200

    # Verificar que los productos se renderizan correctamente en la plantilla
    content = response.content.decode()
    assert producto['nombre'] in content
    assert str(producto['precio']) in content
    assert producto['descripcion'] in content
    assert producto['marca']['nom_marca'] in content
    assert producto['categoria']['nom_categoria'] in content
    assert str(producto['stock']) in content

    # Verificar que no hay errores de mensajes en la respuesta
    assert b'error' not in response.content.lower()
