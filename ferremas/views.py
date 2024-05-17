import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
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

    response = requests.get('http://127.0.0.1:8000/api/productos/get-producto/' + str(id))

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