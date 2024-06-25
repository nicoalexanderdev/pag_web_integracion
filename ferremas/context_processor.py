import requests
from django.conf import settings


def total_carrito(request):
    total = 0
    cantidadTotal = 0 
    if hasattr(request, 'session') and'carrito' in request.session.keys():
        for key, value in request.session['carrito'].items():
            if 'acumulado' in value:  # Verifica si 'acumulado' está presente en el diccionario
                total += int(value['acumulado'])
            if 'cantidad' in value:   # Verifica si 'cantidad' está presente en el diccionario
                cantidadTotal += int(value['cantidad'])
    return {'total_carrito': total, 'cantidad_total': cantidadTotal}

def categorias_processor(request):
    try:
        response = requests.get(f'http://{settings.API_BASE_URL}/get-categorias')
        response.raise_for_status()
        categorias = response.json()
        return {'categorias': categorias}
    except requests.RequestException as e:
        print(f"Error al obtener categorías: {e}")  # Depuración
        return {'categorias': []}
    
def marcas_processor(request):
    try:
        response = requests.get(f'http://{settings.API_BASE_URL}/get-marcas')
        response.raise_for_status()
        marcas = response.json()
        return {'marcas': marcas}
    except requests.RequestException as e:
        print(f'Error al obtener marcas: {e}')
        return {'marcas': []}
    
def regiones(request):
    try:
        response = requests.get(f'http://{settings.API_BASE_TRANSBANK_URL}/region')
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
    