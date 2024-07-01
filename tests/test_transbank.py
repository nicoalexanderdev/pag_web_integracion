from django.test import RequestFactory, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ferremas.Carrito import Carrito
from ferremas.views import transbank
import pytest
import responses
import json
from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware

@pytest.fixture
def authenticated_user():
    user = User.objects.create_user(username='testuser', password='testpass', email='Testuser@example.com')
    return user


@pytest.fixture
def request_factory():
    return RequestFactory()


@pytest.fixture
def req(request_factory, authenticated_user):

    rf = RequestFactory()
    req = rf.get(reverse('transbank'), {'token_ws': 'test_token'})
    req.user = authenticated_user

    # Set up session middleware
    session_middleware = SessionMiddleware(lambda x: x)
    session_middleware.process_request(req)
    req.session['detalles_entrega'] = {
        'tipo_entrega': 'Envío',
        'direccion': '123 Main St',
        'region_id': '7',
        'fecha_entrega': '2023-06-24',
        'costo_despacho': 3990
    }
    req.session['subtotal'] = 36010
    req.session['total_a_pagar'] = 40000
    req.session.save()

    # Assign the subtotal to the request object
    req.subtotal = req.session['subtotal']
    req.total_a_pagar = req.session['total_a_pagar']
    req.detalles_entrega = req.session['detalles_entrega']

    # Simulate the cart with products
    req.carrito = Carrito(req)
    req.carrito.carrito = {
        '1': {'producto_id': 1, 'cantidad': 2},
        '2': {'producto_id': 2, 'cantidad': 1}
    }

    return req


@pytest.mark.django_db
@responses.activate
def test_transbank_valid_token(req):

    # Mock the response from Transbank
    responses.add(
        responses.PUT,
        f'http://{settings.API_BASE_TRANSBANK_URL}/commit/test_token/',
        json={
            'id': 1,
            'status': 'AUTHORIZED',
            'authorization_code': '123456',
            'amount': 40000,
            'buy_order': 'BO-1234',
            'session_id': '1',
            'card_detail': {'card_number': '1234'},
            'accounting_date': '0624',
            'transaction_date': '2023-06-24T12:00:00',
            'payment_type_code': 'VD',
            'response_code': 0,
            'installments_number': 1
        },
        status=200
    )

    responses.add(
        responses.POST,
        f'http://{settings.API_BASE_TRANSBANK_URL}/transaction-save/',
        json={'transaction': {'id': 1}},
        status=200
    )

    responses.add(
        responses.POST,
        f'http://{settings.API_BASE_TRANSBANK_URL}/crear-orden-compra/',
        json={
            'user': req.user.id,
            'subtotal': req.subtotal,
            'costo_despacho': req.detalles_entrega['costo_despacho'],
            'total': req.total_a_pagar,
            'tipo_entrega': req.detalles_entrega['tipo_entrega'],
            'direccion': req.detalles_entrega['direccion'],
            'fecha_entrega': req.detalles_entrega['fecha_entrega'],
            'correo': req.user.email,
            'transaccion': 1,
            'estado': 1
        },
        status=200
    )

    # Mock the response for adding the products to the order
    responses.add(
        responses.POST,
        f'http://{settings.API_BASE_TRANSBANK_URL}/order-items/',
        json={'order': 1, 'producto': 1, 'cantidad': 2},
        status=200
    )

    response = transbank(req)
    content = response.content.decode()
    assert response.status_code == 200
    assert 'Aprobado' in content
    assert '123456' in content
    assert 'BO-1234' in content
    assert '1' in content
    assert '1234' in content

