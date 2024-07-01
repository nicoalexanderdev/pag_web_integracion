from django.test import RequestFactory, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ferremas.views import ir_a_pagar
import pytest
import responses
import json
from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware


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
    req = rf.post(reverse('ir-a-pagar'), {
        'tipo_documento': 'Boleta',
        'forma_pago': 'Webpay'
    })
    req.user = authenticated_user

    # Set up session middleware
    session_middleware = SessionMiddleware(lambda x: x)
    session_middleware.process_request(req)
    req.session.save()

    return req


@pytest.mark.django_db
@responses.activate
def test_ir_a_pagar_post_valid_data(req):

    req.session['total_a_pagar'] = 10000

    api_categorias_url = f'http://{settings.API_BASE_URL}/get-categorias/'
    api_marcas_url = f'http://{settings.API_BASE_URL}/get-marcas/'
    api_dollar_value_url = f'http://{settings.API_BASE_TRANSBANK_URL}/get-dollar-value/'
    api_region_url = f'http://{settings.API_BASE_TRANSBANK_URL}/region/'

    responses.add(responses.GET, api_categorias_url, json=[], status=200)
    responses.add(responses.GET, api_marcas_url, json=[], status=200)
    responses.add(responses.GET, api_dollar_value_url,
                  json={'value': 1.0}, status=200)
    responses.add(responses.GET, api_region_url, json=[], status=200)

    # Mock the response from Transbank
    responses.add(
        responses.POST,
        f'http://{settings.API_BASE_TRANSBANK_URL}/transaction/create/',
        json={'token': 'test_token', 'url': 'https://example.com/payment'},
        status=200
    )

    response = ir_a_pagar(req)
    content = response.content.decode()
    assert response.status_code == 200
    assert 'test_token' in content
    assert 'https://example.com/payment' in content
    assert req.session['forma_de_pago']['tipo_documento'] == 'Boleta'
    assert req.session['forma_de_pago']['forma_pago'] == 'Webpay'


@pytest.mark.django_db
@responses.activate
def test_ir_a_pagar_post_missing_data(req):

    req.POST = {'tipo_documento': '', 'forma_pago': ''}
    req.session['total_a_pagar'] = 10000

    # Mock the response from Transbank
    responses.add(
        responses.POST,
        f'http://{settings.API_BASE_TRANSBANK_URL}/transaction/create/',
        json={'token': 'test_token', 'url': 'https://example.com/payment'},
        status=200
    )

    response = ir_a_pagar(req)
    assert response.status_code == 200
    assert 'forma_de_pago' not in req.session


@pytest.mark.django_db
@responses.activate
def test_ir_a_pagar_post_no_total_a_pagar(req):

    # Mock the response from Transbank
    responses.add(
        responses.POST,
        f'http://{settings.API_BASE_TRANSBANK_URL}/transaction/create/',
        json={'token': 'test_token', 'url': 'https://example.com/payment'},
        status=200
    )

    response = ir_a_pagar(req)
    assert response.status_code == 500
    assert json.loads(response.content)[
        'error'] == 'No se encontró total_a_pagar en la sesión'
