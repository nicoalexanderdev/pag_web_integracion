from django.test import RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from ferremas.views import agregar_detalles_entrega
import pytest
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.storage.fallback import FallbackStorage

@pytest.fixture
def authenticated_user():
    user = User.objects.create_user(username='testuser', password='testpass')
    return user

@pytest.fixture
def request_factory():
    return RequestFactory()

@pytest.fixture
def req(request_factory, authenticated_user):
    rf = RequestFactory()
    req = rf.post(reverse('agregar_detalles_entrega'), {
        'tipo_entrega': 'Retiro',
        'direccion': '123 Main St',
        'region_id': '7'
    })
    req.user = authenticated_user

    # Set up session middleware
    session_middleware = SessionMiddleware(lambda x: x)
    session_middleware.process_request(req)
    req.session.save()

    # Set up message middleware
    message_storage = FallbackStorage(req)
    setattr(req, '_messages', message_storage)

    return req

@pytest.mark.django_db
def test_agregar_detalles_entrega_post_retiro(req):
    response = agregar_detalles_entrega(req)
    assert response.status_code == 302
    assert response.url == reverse('pago')
    assert req.session['detalles_entrega']['tipo_entrega'] == 'Retiro'
    assert req.session['detalles_entrega']['direccion'] == '123 Main St'
    assert req.session['detalles_entrega']['region_id'] == '7'
    assert req.session['detalles_entrega']['costo_despacho'] == 0

@pytest.mark.django_db
def test_agregar_detalles_entrega_post_region_7(req):
    req.POST = {'tipo_entrega': 'Envío', 'direccion': '123 Main St', 'region_id': '7'}
    response = agregar_detalles_entrega(req)
    assert response.status_code == 302
    assert response.url == reverse('pago')
    assert req.session['detalles_entrega']['tipo_entrega'] == 'Envío'
    assert req.session['detalles_entrega']['direccion'] == '123 Main St'
    assert req.session['detalles_entrega']['region_id'] == '7'
    assert req.session['detalles_entrega']['costo_despacho'] == 3990

@pytest.mark.django_db
def test_agregar_detalles_entrega_post_other_region(req):
    req.POST = {'tipo_entrega': 'Envío', 'direccion': '123 Main St', 'region_id': '8'}
    response = agregar_detalles_entrega(req)
    assert response.status_code == 302
    assert response.url == reverse('pago')
    assert req.session['detalles_entrega']['tipo_entrega'] == 'Envío'
    assert req.session['detalles_entrega']['direccion'] == '123 Main St'
    assert req.session['detalles_entrega']['region_id'] == '8'
    assert req.session['detalles_entrega']['costo_despacho'] == 5990

@pytest.mark.django_db
def test_agregar_detalles_entrega_post_missing_fields(req):
    req.POST = {'tipo_entrega': '', 'direccion': ''}
    response = agregar_detalles_entrega(req)
    assert response.status_code == 302
    assert response.url == reverse('checkout')