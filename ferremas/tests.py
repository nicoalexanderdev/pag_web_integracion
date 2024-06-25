import json
from django.test import TestCase, RequestFactory, Client
from django.conf import settings
from unittest.mock import patch
import requests
from .views import index
from .context_processor import total_carrito, get_dollar
from django.urls import reverse
from django.http import HttpResponseRedirect

class TestIndexView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()

    @patch('requests.get')
    def test_index_success(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = [{'id': 1, 'name': 'Product 1'}, {'id': 2, 'name': 'Product 2'}]

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/home.html')

    @patch('requests.get')
    def test_index_api_error(self, mock_get):
        mock_get.side_effect = requests.RequestException('Mocked API error')

        response = self.client.get('/')
        self.assertEqual(response.status_code, 500)
        self.assertTemplateNotUsed(response, 'app/home.html')  

    def test_total_carrito(self):
        # Simular una sesión con datos de carrito
        request = self.factory.get('/')
        request.session = {'carrito': {'1': {'acumulado': '10', 'cantidad': '2'}, '2': {'acumulado': '5', 'cantidad': '1'}}}

        # Llamar al context processor
        context = total_carrito(request)

        # Verificar el resultado esperado
        self.assertEqual(context['total_carrito'], 15)
        self.assertEqual(context['cantidad_total'], 3)

class TestDetalleProductoView(TestCase):

    @patch('requests.get')
    def test_detalle_producto_success(self, mock_get):
        mock_response = requests.models.Response()
        mock_response.status_code = 200
        mock_response.json = lambda: {'id': 1, 'nombre': 'Producto de prueba'}
        mock_get.return_value = mock_response

        response = self.client.get(reverse('detalle_producto', args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/detalle-producto.html')
        self.assertIn('producto', response.context)
        self.assertEqual(response.context['producto']['id'], 1)

    @patch('requests.get')
    def test_detalle_producto_api_error(self, mock_get):
        mock_response = requests.models.Response()
        mock_response.status_code = 404  # Simular un error 404 desde la API
        mock_get.return_value = mock_response

        response = self.client.get(reverse('detalle_producto', args=[1]))

        self.assertRedirects(response, reverse('home'))
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Error al obtener detalles del producto')

    @patch('requests.get', side_effect=requests.RequestException('Mocked API error'))
    def test_detalle_producto_request_exception(self, mock_get):
        response = self.client.get(reverse('detalle_producto', args=[1]))

        self.assertRedirects(response, reverse('home'))
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Error de conexión: Mocked API error')