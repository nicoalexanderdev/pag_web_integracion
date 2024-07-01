import json
from django.test import RequestFactory, TestCase, Client
from django.conf import settings
from unittest.mock import patch
from unittest import mock
import requests
from .views import index, detalle_producto, checkout
from .context_processor import total_carrito, get_dollar
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponseServerError
from django.template.loader import render_to_string
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware



class IndexViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.api_url = f'http://{settings.API_BASE_URL}/'

    @patch('requests.get')
    def test_index_view_success(self, mock_get):

        productos = [
            {'id': 1, 'nombre': 'Producto 1', 'precio': 1000, 'descripcion': 'Descripción del Producto 1'},
            {'id': 2, 'nombre': 'Producto 2', 'precio': 2000, 'descripcion': 'Descripción del Producto 2'}
        ]
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = productos

        response = self.client.get(reverse('home'))  
        
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'app/home.html')

        self.assertEqual(response.context['productos'], productos)

    @patch('requests.get')
    def test_index_view_api_error(self, mock_get):

        mock_get.side_effect = requests.exceptions.RequestException

        response = self.client.get(reverse('home'))
        
        self.assertEqual(response.status_code, 500)

        expected_error_message = {'error': 'Error al obtener datos de la API: '}
        self.assertJSONEqual(response.content, expected_error_message)




class DetalleProductoViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.producto_id = 1
        self.api_url = f'http://{settings.API_BASE_URL}/get-producto/{self.producto_id}/'
    
    @patch('requests.get')
    def test_detalle_producto_success(self, mock_get):
        # Datos del producto simulado que esperamos recibir de la API
        producto = {'id': 1, 'nombre': 'Producto 1', 'precio': 1000, 'descripcion': 'Descripción del Producto 1'}

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = producto

        response = self.client.get(reverse('detalle_producto', args=[self.producto_id]), follow=True)
        
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'app/detalle-producto.html')

        self.assertEqual(response.context['producto'], producto)
