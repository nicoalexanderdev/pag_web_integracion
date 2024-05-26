import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from ferremas.Carrito import Carrito
import requests
from django.conf import settings
from ferremas.Webpay import transbank_create, transaction_commit
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages

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


def categoria(request, id):
    try:
        response = requests.get(f'http://{settings.API_BASE_URL}/get-productos-categoria/{id}')
        response.raise_for_status()  # Esto lanzará una excepción si la respuesta no es 2xx
        productos = response.json()

        # Verificar que la respuesta contiene los datos esperados
        if 'categoria' in productos and 'productos' in productos:
            data = {
                'categoria': productos['categoria'],
                'productos': productos['productos']
            }
            return render(request, 'app/categoria.html', data)
        else:
            # Manejo de caso en el que los datos esperados no están presentes
            return redirect('home')
    except requests.RequestException as e:
        # Registrar el error, puedes usar logging en lugar de print
        print(f"Error al obtener productos de la API: {e}")
        return redirect('home')


def marca(request, id):
    try:
        response = requests.get(f'http://{settings.API_BASE_URL}/get-productos-marca/{id}')
        response.raise_for_status()  # Esto lanzará una excepción si la respuesta no es 2xx
        productos = response.json()

        # Verificar que la respuesta contiene los datos esperados
        if 'marca' in productos and 'productos' in productos:
            data = {
                'marca': productos['marca'],
                'productos': productos['productos']
            }
            return render(request, 'app/marca.html', data)
        else:
            # Manejo de caso en el que los datos esperados no están presentes
            return redirect('home')
    except requests.RequestException as e:
        # Registrar el error, puedes usar logging en lugar de print
        print(f"Error al obtener productos de la API: {e}")
        return redirect('home')


def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(request.POST)
        if formulario.is_valid():
            user = formulario.save()
            # Autenticar y iniciar sesión al usuario recién registrado
            username = formulario.cleaned_data.get('username')
            raw_password = formulario.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Te has registrado correctamente')
                return redirect(to='home')
        else:
            messages.error(request, 'No se ha podido registrar, intente nuevamente')
                
        data['form'] = formulario

    return render(request, 'registration/registro.html', data)


# crud carrito


def agregar_carrito(request, id):
    carrito = Carrito(request)

    # Realiza la solicitud a la API para obtener los datos del producto
    response = requests.get( f'http://{settings.API_BASE_URL}/get-producto/{id}')
    if response.status_code == 200:
        producto_data = response.json()
        carrito.agregar(producto_data)
        
        # Redirigir de vuelta a la página desde donde se envió la solicitud
        referer_url = request.META.get('HTTP_REFERER')
        if referer_url:
            return HttpResponseRedirect(referer_url)
        else:
            return redirect('home')  # Redirigir a home si no hay referencia
        
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



# Transbank views


@csrf_exempt
def transbank(request):

    # Capturar el token proporcionado por Webpay en la URL de retorno
    tokenws = request.GET.get('token_ws')

    # levantamos error en caso que no se encuentra el token proporcionado
    if not tokenws:
        return JsonResponse({'error': 'No se proporciono token_ws'}, status=400)

    # Realizar la solicitud de commit de la transacción
    response_data = transaction_commit(tokenws)

    # control de error en la solicitud de commit de la transacción
    if 'error' in response_data:
        return JsonResponse(response_data, status=500)
    
    # diccionario de mapeo de status de error
    status_mapping = {
        'FAILED': 'Transacción cancelada o rechazada',
        'REJECTED': 'Transacción cancelada o rechazada',
        'CANCELLED': 'Transacción cancelada o rechazada',
    }

    # obtenemos las respuestas desde reponse_data
    status = response_data.get('status')
    authorization_code = response_data.get('authorization_code')
    amount = response_data.get('amount')
    buy_order = response_data.get('buy_order')
    session_id = response_data.get('session_id')
    card_number = response_data.get('card_detail', {}).get('card_number')
    accounting_date = response_data.get('accounting_date')
    transaction_date = response_data.get('transaction_date')
    payment_type_code = response_data.get('payment_type_code')
    response_code = response_data.get('response_code')
    installments_number = response_data.get('installments_number')
    user = request.user.id

    # creamos diccionario para guardar los datos de la transaccion en la base de datos
    data_db = {
        "user": user,
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "status": status,
        "card_number": card_number,
        "accounting_date": accounting_date,
        "transaction_date": transaction_date,
        "authorization_code": authorization_code,
        "payment_type_code": payment_type_code,
        "response_code": response_code,
        "installments_number": installments_number
    }

    print(data_db)

    # guardamos en la base de datos
    try:
        response = requests.post(f'http://{settings.API_BASE_TRANSBANK_URL}/transaction-save/', json=data_db)
        response.raise_for_status()
        response_data = response.json()
        print(response_data)
    except requests.RequestException as e:
        print(f"Error al guardar la transacción en la base de datos: {e}")
        return JsonResponse({'error': 'Error al guardar la transacción en la base de datos'}, status=500)

   # Manejamos el caso en que la transacción es cancelada
    if status in status_mapping:
        data = {
            "resultado": status_mapping[status],
            "codigo": authorization_code,
            "monto": amount
        }
        return render(request, 'app/transbank.html', data)
    
    # data si todo sale bien
    data = {
        "resultado": status,
        "codigo": authorization_code,
        "monto": amount
    }

    # limpiamos el carrito
    carrito = Carrito(request)
    carrito.limpiar()  

    return render(request, 'app/transbank.html', data)
    


@login_required
def ir_a_pagar(request):
    # Realizar la solicitud para crear la transacción en Transbank
    response_data = transbank_create(request)
    
    # verificamos recibir el token y la url
    if 'token' in response_data and 'url' in response_data:
        token = response_data['token']
        url = response_data['url']

        # Pasar la URL y el token a la plantilla
        data = {
            "url": url,
            "token": token
        }

        return render(request, 'app/redirect_to_transbank.html', data)
    else:
        # Manejamos el caso en el que la respuesta de transbank_create no contiene el token o la URL
        return JsonResponse({'error': 'No se recibió el token o la URL de Transbank'}, status=500)
