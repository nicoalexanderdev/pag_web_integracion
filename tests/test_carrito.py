import pytest
from django.http import HttpRequest
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django.urls import reverse
from django.contrib.messages.middleware import MessageMiddleware
from unittest.mock import patch
from ferremas.Carrito import Carrito
from ferremas.views import agregar_carrito, eliminar_carrito, restar_carrito, limpiar_carrito
from django.test import Client, RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage


@pytest.fixture
def producto():
    return {
        'id': 1,
        'nombre': 'Producto Test',
        'precio': 100,
        'marca': {'id': 1, 'nom_marca': 'Marca Test'},
        'categoria': {'id': 1, 'nom_categoria': 'Categoria Test'},
        'image_url': 'http://example.com/image.jpg'
    }


# set up de la session en middleware
@pytest.fixture
def request_rf(db):
    rf = RequestFactory()
    request = rf.get('/')
    def get_response(request): return None

    # Process request through SessionMiddleware
    session_middleware = SessionMiddleware(get_response)
    session_middleware.process_request(request)
    request.session.save()

    # Process request through AuthenticationMiddleware
    auth_middleware = AuthenticationMiddleware(get_response)
    auth_middleware.process_request(request)

    # Process request through MessageMiddleware
    messages_middleware = MessageMiddleware(get_response)
    messages_middleware.process_request(request)

    # Set an anonymous user or a test user if needed
    request.user = AnonymousUser()

    # Set up message storage for the request
    setattr(request, 'session', request.session)
    messages_storage = FallbackStorage(request)
    setattr(request, '_messages', messages_storage)

    return request


@pytest.mark.django_db
def test_agregar_producto_carrito(request_rf, producto):
    carrito = Carrito(request_rf)
    carrito.agregar(producto)
    assert str(producto['id']) in carrito.carrito
    assert carrito.carrito[str(producto['id'])]['cantidad'] == 1


@pytest.mark.django_db
def test_eliminar_producto_carrito(request_rf, producto):
    carrito = Carrito(request_rf)
    carrito.agregar(producto)
    carrito.eliminar(producto)
    assert str(producto['id']) not in carrito.carrito


@pytest.mark.django_db
def test_restar_producto_carrito(request_rf, producto):
    carrito = Carrito(request_rf)
    carrito.agregar(producto)
    carrito.agregar(producto)
    carrito.restar(producto)
    assert carrito.carrito[str(producto['id'])]['cantidad'] == 1
    carrito.restar(producto)
    assert str(producto['id']) not in carrito.carrito


@pytest.mark.django_db
def test_limpiar_carrito(request_rf, producto):
    carrito = Carrito(request_rf)
    carrito.agregar(producto)

    assert len(carrito.carrito) == 1

    carrito.limpiar()

    request_rf.session.save()

    carrito = Carrito(request_rf)
    assert carrito.carrito == {}




# test de las funcioens del carro en las views



@pytest.mark.django_db
@patch('requests.get')
def test_agregar_carrito_view(mock_get, request_rf, producto):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = producto

    # agregamos un producto
    request = request_rf
    request.path = reverse('agregar-carrito', args=[producto['id']])

    response = agregar_carrito(request, producto['id'])
    assert response.status_code == 302 

    carrito = Carrito(request)
    assert str(producto['id']) in carrito.carrito


@pytest.mark.django_db
@patch('requests.get')
def test_eliminar_carrito_view(mock_get, request_rf, producto):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = producto

    request = request_rf
    request.path = reverse('eliminar-carrito', args=[producto['id']])

    # agregamos un producto
    agregar_carrito(request, producto['id'])
    carrito = Carrito(request)
    assert str(producto['id']) in carrito.carrito

    # eliminamos el producto
    response = eliminar_carrito(request, producto)
    assert response.status_code == 302

    # vrificamos
    carrito = Carrito(request)
    assert str(producto['id']) not in carrito.carrito


@pytest.mark.django_db
@patch('requests.get')
def test_restar_carrito_view(mock_get, request_rf, producto):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = producto

    # agregamos un producto
    request = request_rf
    request.path = reverse('agregar-carrito', args=[producto['id']])

    agregar_carrito(request, producto['id'])
    agregar_carrito(request, producto['id'])
    carrito = Carrito(request)
    assert str(producto['id']) in carrito.carrito
    assert carrito.carrito[str(producto['id'])]['cantidad'] == 2

    # restamos producto del carro
    request.path = reverse('restar-carrito', args=[producto['id']])
    response = restar_carrito(request, producto['id'])
    assert response.status_code == 302  

    # verificamos si funciono
    carrito = Carrito(request)  
    assert carrito.carrito[str(producto['id'])]['cantidad'] == 1


@pytest.mark.django_db
@patch('requests.get')
def test_limpiar_carrito_view(mock_get, request_rf, producto):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = producto

    # agregamos un producto
    request = request_rf
    request.path = reverse('agregar-carrito', args=[producto['id']])

    agregar_carrito(request, producto['id'])
    carrito = Carrito(request)
    assert str(producto['id']) in carrito.carrito

    # limpiamos el carro
    request.path = reverse('limpiar-carrito')
    response = limpiar_carrito(request)
    assert response.status_code == 302 

    # verificamos
    carrito = Carrito(request)  
    assert carrito.carrito == {}
