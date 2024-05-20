from django.http import JsonResponse
import requests
import random
from django.conf import settings
from ferremas.Carrito import Carrito
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token

def headers_request_transbank():
  headers = { # DEFINICIÓN TIPO DE AUTORIZACIÓN Y AUTENTICACIÓN
                "Authorization": "Token",

                # LLAVE QUE DEBE SER MODIFICADA PORQUE ES SOLO DEL AMBIENTE DE INTEGRACIÓN DE TRANSBANK (PRUEBAS)
                "Tbk-Api-Key-Id": "597055555532",

                # LLAVE QUE DEBE SER MODIFICADA PORQUE DEL AMBIENTE DE INTEGRACIÓN DE TRANSBANK (PRUEBAS)
                "Tbk-Api-Key-Secret": "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",

                # DEFINICIÓN DEL TIPO DE INFORMACIÓN ENVIADA
                "Content-Type": "application/json",

                # DEFINICIÓN DE RECURSOS COMPARTIDOS ENTRE DISTINTOS SERVIDORES PARA CUALQUIER MÁQUINA
                "Access-Control-Allow-Origin": "*",
                'Referrer-Policy': 'origin-when-cross-origin',
                } 
  return headers   


@login_required
def transbank_create(request):
    # Obtener el carrito asociado al usuario
    carrito = Carrito(request)
    user = request.user

    # Crear orden de compra
    buy_order = f"BO-{random.randint(1000, 9999)}"
    session_id = str(user.id)
    amount = sum(item['acumulado'] for item in carrito.carrito.values())
    return_url = f"http://{settings.TRANSBANK_RETURN_URL}"

    data = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": amount,
        "return_url": return_url
    }

    # Realizar la solicitud a la API de Transbank
    headers = headers_request_transbank()
    response = requests.post(f'http://{settings.API_BASE_TRANSBANK_URL}/transaction/create/', json=data, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        token = response_data.get('token')
        url = response_data.get('url')

        # Imprimir el token y la URL de respuesta
        print('Token:', token)
        print('URL:', url)

        return response_data

    else:
        return JsonResponse({'error': 'Error al crear la transacción'}, status=response.status_code)



def transaction_commit(tokenws):
    try:
        # Realizar la solicitud a la API de Transbank para confirmar la transacción
        url = f"http://{settings.API_BASE_TRANSBANK_URL}/commit/{tokenws}"
        headers = headers_request_transbank()
        response = requests.put(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': 'Error al confirmar la transacción'}
    except Exception as e:
        print(f"Error al confirmar transacción en Transbank: {e}")
        return {'error': str(e)}