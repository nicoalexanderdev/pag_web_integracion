import requests
from django.conf import settings


def total_carrito(request):
    total = 0
    cantidadTotal = 0 
    if request:
        if 'carrito' in request.session.keys():
            for key, value in request.session['carrito'].items():
                total += int(value['acumulado'])
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