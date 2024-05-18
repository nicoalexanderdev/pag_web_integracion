import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from ferremas.Carrito import Carrito
import requests

# Create your views here.


def index(request):
    try:
        productos = requests.get('http://127.0.0.1:8000/api/productos/').json()
        data = {
            'productos': productos,
        }
        return render(request, 'app/home.html', data)
    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Error de decodificación JSON: {}'.format(str(e))}, status=500)


def detalle_producto(request, id):

    response = requests.get(
        'http://127.0.0.1:8000/api/productos/get-producto/' + str(id))

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
    response = requests.get(f'http://127.0.0.1:8000/api/productos/get-producto/{id}')
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
    response = requests.get(f'http://127.0.0.1:8000/api/productos/get-producto/{id}')
    if response.status_code == 200:
        producto_data = response.json()
        carrito.eliminar(producto_data['id'])
        return render(request, 'app/checkout.html')
    else:
        # Si la solicitud a la API falla, redirige a una página de error o muestra un mensaje de error
        return HttpResponseRedirect(reverse('home'))

def restar_carrito(request, id):
    carrito = Carrito(request)
    response = requests.get(f'http://127.0.0.1:8000/api/productos/get-producto/{id}')

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