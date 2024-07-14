from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
import requests
from django.core.paginator import Paginator


def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('index')
            else:
                messages.error(
                    request, 'No tienes permisos para acceder a esta área.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'app/admin_login.html')


@user_passes_test(lambda u: u.is_staff)
def index(request):
    return render(request, 'app/index.html')


def listar_productos(request):
    headers = {'Authorization': settings.API_TOKEN}
    page = request.GET.get('page', 1)
    media = settings.MEDIA_URL
    try:
        response = requests.get(f'http://{settings.API_BASE_URL}/', headers=headers)
        response.raise_for_status()
        productos = response.json()

        try:
            paginator = Paginator(productos, 5)
            productos = paginator.page(page)
        except:
            raise Http404
        
        data = {
            'entity': productos,
            'paginator': paginator,
            'media': media
        }
        return render(request, 'app/crud_productos/listar.html', data)
    except:
        messages.error(request, 'Error al obtener productos')
        return redirect('index')
    

def agregar_producto(request):
    headers = {'Authorization': settings.API_TOKEN,}
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        categoria = request.POST.get('categoria')
        marca = request.POST.get('marca')
        descripcion = request.POST.get('descripcion')

        files = {'image_url': request.FILES['imagen']} if 'imagen' in request.FILES else None

        print(f'Datos recibidos: {nombre}, {precio}, {stock}, {categoria}, {marca}, {descripcion}, {files}')

        payload = {
            'nombre': nombre,
            'precio': precio,
            'descripcion': descripcion,
            'stock': stock,
            'marca': marca,
            'categoria': categoria,
        }

        try:
            response = requests.post(
                f'http://{settings.API_BASE_URL}/create-producto/',
                data=payload,
                files=files,
                headers=headers
            )
                
            response.raise_for_status()
            print(f'Respuesta de la API: {response.json()}')
            messages.success(request, 'Producto agregado correctamente')
            return redirect('productos')
        except requests.exceptions.HTTPError as e:
            print('Error al guardar producto ', e)
            try:
                print('Detalles del error: ', e.response.json())  # Obtener más detalles del error
            except ValueError:
                print('No se pudo obtener detalles del error en formato JSON')
            messages.error(request, 'Hubo un error')
            return redirect('productos')

    return render(request, 'app/crud_productos/agregar.html')



def modificar_producto(request, id):
    headers = {'Authorization': settings.API_TOKEN}
    media = settings.MEDIA_URL

    try:
        response = requests.get(f'http://{settings.API_BASE_URL}/get-producto/{id}/', headers=headers)
        response.raise_for_status()
        producto = response.json()

        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            precio = request.POST.get('precio')
            stock = request.POST.get('stock')
            categoria = request.POST.get('categoria')
            marca = request.POST.get('marca')
            descripcion = request.POST.get('descripcion')

            files = {'image_url': request.FILES['imagen']} if 'imagen' in request.FILES else None

            print(f'Datos recibidos: {nombre}, {precio}, {stock}, {categoria}, {marca}, {descripcion}, {files}')

            payload = {
                'nombre': nombre,
                'precio': precio,
                'descripcion': descripcion,
                'stock': stock,
                'marca': marca,
                'categoria': categoria,
            }

            try:
                response = requests.put(
                    f'http://{settings.API_BASE_URL}/update-producto/{id}/',
                    data=payload,
                    files=files,
                    headers=headers
                )
                    
                response.raise_for_status()
                print(f'Respuesta de la API: {response.json()}')
                messages.success(request, 'Producto modificado correctamente')
                return redirect('productos')
            except requests.exceptions.HTTPError as e:
                print('Error al modificar producto ', e)
                try:
                    print('Detalles del error: ', e.response.json())  # Obtener más detalles del error
                except ValueError:
                    print('No se pudo obtener detalles del error en formato JSON')
                messages.error(request, 'Hubo un error')
                return redirect('productos')

        data = {
            'producto': producto,
            'media': media,
        }
        return render(request, 'app/crud_productos/modificar.html', data)
    except requests.exceptions.HTTPError as e:
        print('Error al obtener producto: ', e)
        return redirect('productos')



def eliminar_producto(request, id):
    headers = {'Authorization': settings.API_TOKEN}
    try:
        response = requests.delete(f'http://{settings.API_BASE_URL}/delete-producto/{id}/', headers=headers)
        response.raise_for_status()
        messages.success(request, "Eliminado Correctamente")
        return redirect('productos')
    
    except requests.exceptions.HTTPError as e:
        print('Error al eliminar producto ', e)
        try:
            print('Detalles del error: ', e.response.json())
        except ValueError:
            print('No se pudo obtener detalles del error en formato JSON')
        messages.error(request, 'Hubo un error al eliminar')
        return redirect('productos')
