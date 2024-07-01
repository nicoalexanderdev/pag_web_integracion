import requests
from django.conf import settings


def total_carrito(request):
    total = 0
    cantidadTotal = 0 
    costo_despacho = 0
    subtotal = 0
    
    if hasattr(request, 'session') and 'carrito' in request.session.keys():
        for key, value in request.session['carrito'].items():
            if 'acumulado' in value:  # Verifica si 'acumulado' está presente en el diccionario
                subtotal += int(value['acumulado'])
            if 'cantidad' in value:   # Verifica si 'cantidad' está presente en el diccionario
                cantidadTotal += int(value['cantidad'])

    if hasattr(request, 'session') and 'detalles_entrega' in request.session:
        costo_despacho = request.session['detalles_entrega'].get('costo_despacho', 0)
    
    total = subtotal + costo_despacho

    request.session['total_a_pagar'] = total
    request.session['subtotal'] = subtotal

    return {
        'subtotal': subtotal,
        'cantidad_total': cantidadTotal,
        'costo_despacho': costo_despacho,
        'total_a_pagar': total,
    }


def categorias_processor(request):
    try:
        response = requests.get(f'http://{settings.API_BASE_URL}/get-categorias/')
        response.raise_for_status()
        categorias = response.json()
        return {'categorias': categorias}
    except requests.RequestException as e:
        print(f"Error al obtener categorías: {e}")
        return {'categorias': []}
    
def marcas_processor(request):
    try:
        response = requests.get(f'http://{settings.API_BASE_URL}/get-marcas/')
        response.raise_for_status()
        marcas = response.json()
        return {'marcas': marcas}
    except requests.RequestException as e:
        print(f'Error al obtener marcas: {e}')
        return {'marcas': []}
    
def regiones(request):
    try:
        response = requests.get(f'http://{settings.API_BASE_TRANSBANK_URL}/region/')
        response.raise_for_status()  # Raise an exception for HTTP errors
        regiones = response.json()
        return {'regiones': regiones}
    except requests.RequestException as e:
        print(f'Error al obtener regiones: {e}')
        return {'regiones': []}

    
def get_dollar(request):
    try:
        response = requests.get(f'http://{settings.API_BASE_TRANSBANK_URL}/get-dollar-value/')
        response.raise_for_status()
        valor_dolar = response.json()

        if 'value' in valor_dolar:
            return {'valor_dolar': float(valor_dolar['value'])}  
        else:
            return {'valor_dolar': None}

    except requests.RequestException as e:
        print(f'Error al obtener valor del dolar actualizado: {e}')
        return {'valor_dolar': None} 
    