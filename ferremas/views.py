import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from ferremas.Carrito import Carrito
import requests
from django.conf import settings
from ferremas.Webpay import transbank_create, transaction_commit
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    try:
        productos = requests.get(f'http://{settings.API_BASE_URL}').json()
        data = {
            'productos': productos,
        }
        return render(request, 'app/home.html', data)
    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Error de decodificación JSON: {}'.format(str(e))}, status=500)


def detalle_producto(request, id):

    response = requests.get(
        f'http://{settings.API_BASE_URL}/get-producto/{id}')

    if response.status_code == 200:

        producto = response.json()

        data = {
            'producto': producto,
        }

        return render(request, 'app/detalle-producto.html', data)
    else:
        # Si la solicitud no fue exitosa, redirigir a una página de error
        # O mostrar un mensaje de error al usuario
        return HttpResponseRedirect(reverse('home'))
    

def checkout(request):
    context = {}
    return render(request, 'app/checkout.html')


# crud carrito


def agregar_carrito(request, id):
    carrito = Carrito(request)

    # Realiza la solicitud a la API para obtener los datos del producto
    response = requests.get( f'http://{settings.API_BASE_URL}/get-producto/{id}')
    if response.status_code == 200:
        producto_data = response.json()
        carrito.agregar(producto_data)
        return render(request, 'app/checkout.html')
    else:
        # Si la solicitud a la API falla, redirige a una página de error o muestra un mensaje de error
        return HttpResponseRedirect(reverse('home'))

    
def eliminar_carrito(request, id):
    carrito = Carrito(request)
    # Realiza la solicitud a la API para obtener los datos del producto
    response = requests.get( f'http://{settings.API_BASE_URL}/get-producto/{id}')
    if response.status_code == 200:
        producto_data = response.json()
        carrito.eliminar(producto_data['id'])
        return render(request, 'app/checkout.html')
    else:
        # Si la solicitud a la API falla, redirige a una página de error o muestra un mensaje de error
        return HttpResponseRedirect(reverse('home'))


def restar_carrito(request, id):
    carrito = Carrito(request)
    response = requests.get( f'http://{settings.API_BASE_URL}/get-producto/{id}')

    if response.status_code == 200:
        producto_data = response.json()
        carrito.restar(producto_data)
        return render(request, 'app/checkout.html')
    else:
        # Si la solicitud a la API falla, redirige a una página de error o muestra un mensaje de error
        return HttpResponseRedirect(reverse('home'))


def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()  # Llama al método limpiar directamente
    return render(request, 'app/checkout.html')


def transbank(request):
    # Captura los parámetros proporcionados por Webpay
    resultado_transaccion = request.GET.get('status')
    codigo_autorizacion = request.GET.get('buy_order')
    monto_pagado = request.GET.get('amount')

    # guardaremos en la base de datos

    data = {
        "resultado": resultado_transaccion,
        "codigo": codigo_autorizacion,
        "monto": monto_pagado
    }

    
    return render(request, 'app/transbank.html', data)

@login_required
def ir_a_pagar(request):
    # Realizar la solicitud para crear la transacción en Transbank
    response_data = transbank_create(request)
    
    if 'token' in response_data and 'url' in response_data:
        token = response_data['token']
        url = response_data['url']

        # Imprimir el token y la URL de respuesta
        print('Token:', token)
        print('URL:', url)

        # Llamar a la función para confirmar la transacción
        transaction_commit(request, token)

        # Pasar la URL y el token a la plantilla
        data = {
            "url": url,
            "token": token
        }

        return render(request, 'app/redirect_to_transbank.html', data)
    else:
        # Manejar el caso en el que la respuesta de transbank_create no contiene el token o la URL
        return JsonResponse({'error': 'No se recibió el token o la URL de Transbank'}, status=500)
