from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
import requests
from django.core.paginator import Paginator
from openpyxl import Workbook


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


@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def index(request):
    return render(request, 'app/index.html')


@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
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


@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
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


@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
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


@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
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


@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def listar_marcas(request):
    headers = {'Authorization': settings.API_TOKEN}

    try:
        response = requests.get(f'http://{settings.API_BASE_URL}/get-marcas/', headers=headers)
        response.raise_for_status()
        marcas = response.json()
        
        data = {
            'marcas': marcas,
        }
        return render(request, 'app/crud_marcas/listar.html', data)
    except:
        messages.error(request, 'Error al obtener marcas')
        return redirect('index')


@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def agregar_marca(request):
    headers = {'Authorization': settings.API_TOKEN,}
    
    if request.method == 'POST':
        nom_marca = request.POST.get('nom_marca')

        payload = {
            'nom_marca': nom_marca
        }

        try:
            response = requests.post(
                f'http://{settings.API_BASE_URL}/create-marca/',
                data=payload,
                headers=headers
            )
                
            response.raise_for_status()
            print(f'Respuesta de la API: {response.json()}')
            messages.success(request, 'Marca agregado correctamente')
            return redirect('marcas')
        
        except requests.exceptions.HTTPError as e:
            print('Error al guardar marca ', e)
            try:
                print('Detalles del error: ', e.response.json())  # Obtener más detalles del error
            except ValueError:
                print('No se pudo obtener detalles del error en formato JSON')
            messages.error(request, 'Hubo un error')
            return redirect('marcas')
        
    return render(request, 'app/crud_marcas/agregar.html')  


@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def modificar_marca(request, id):

    headers = {'Authorization': settings.API_TOKEN}

    try:
        response = requests.get(f'http://{settings.API_BASE_URL}/get-marca/{id}/', headers=headers)
        response.raise_for_status()
        marca = response.json()

        if request.method == 'POST':
            nom_marca = request.POST.get('nom_marca')

            payload = {
                'nom_marca': nom_marca,

            }

            try:
                response = requests.put(
                    f'http://{settings.API_BASE_URL}/update-marca/{id}/',
                    data=payload,
                    headers=headers
                )
                    
                response.raise_for_status()
                print(f'Respuesta de la API: {response.json()}')
                messages.success(request, 'Marca modificada correctamente')
                return redirect('marcas')
            
            except requests.exceptions.HTTPError as e:
                print('Error al modificar marca ', e)
                try:
                    print('Detalles del error: ', e.response.json())  # Obtener más detalles del error
                except ValueError:
                    print('No se pudo obtener detalles del error en formato JSON')
                messages.error(request, 'Hubo un error')
                return redirect('marcas')

        data = {
            'marca': marca,
        }
        return render(request, 'app/crud_marcas/modificar.html', data)
    
    except requests.exceptions.HTTPError as e:
        print('Error al obtener marca: ', e)
        return redirect('marcas')


@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def eliminar_marca(request, id):
    headers = {'Authorization': settings.API_TOKEN}
    try:
        response = requests.delete(f'http://{settings.API_BASE_URL}/delete-marca/{id}/', headers=headers)
        response.raise_for_status()
        messages.success(request, "Eliminado Correctamente")
        return redirect('marcas')
    
    except requests.exceptions.HTTPError as e:
        print('Error al eliminar marca ', e)
        try:
            print('Detalles del error: ', e.response.json())
        except ValueError:
            print('No se pudo obtener detalles del error en formato JSON')
        messages.error(request, 'Hubo un error al eliminar')
        return redirect('marcas')


@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def listar_categorias(request):
    headers = {'Authorization': settings.API_TOKEN}

    try:
        response = requests.get(f'http://{settings.API_BASE_URL}/get-categorias/', headers=headers)
        response.raise_for_status()
        categorias = response.json()
        
        data = {
            'categorias': categorias,
        }
        return render(request, 'app/crud_categorias/listar.html', data)
    except:
        messages.error(request, 'Error al obtener categorias')
        return redirect('index')


@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def agregar_categoria(request):
    headers = {'Authorization': settings.API_TOKEN,}
    
    if request.method == 'POST':
        nom_categoria = request.POST.get('nom_categoria')

        payload = {
            'nom_categoria': nom_categoria
        }

        try:
            response = requests.post(
                f'http://{settings.API_BASE_URL}/create-categoria/',
                data=payload,
                headers=headers
            )
                
            response.raise_for_status()
            print(f'Respuesta de la API: {response.json()}')
            messages.success(request, 'Categoria agregada correctamente')
            return redirect('categorias')
        
        except requests.exceptions.HTTPError as e:
            print('Error al guardar categoria', e)
            try:
                print('Detalles del error: ', e.response.json())  # Obtener más detalles del error
            except ValueError:
                print('No se pudo obtener detalles del error en formato JSON')
            messages.error(request, 'Hubo un error')
            return redirect('categorias')
        
    return render(request, 'app/crud_categorias/agregar.html')  


@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def modificar_categoria(request, id):

    headers = {'Authorization': settings.API_TOKEN}

    try:
        response = requests.get(f'http://{settings.API_BASE_URL}/get-categoria/{id}/', headers=headers)
        response.raise_for_status()
        categoria = response.json()

        if request.method == 'POST':
            nom_categoria = request.POST.get('nom_categoria')

            payload = {
                'nom_categoria': nom_categoria,
            }

            try:
                response = requests.put(
                    f'http://{settings.API_BASE_URL}/update-categoria/{id}/',
                    data=payload,
                    headers=headers
                )
                    
                response.raise_for_status()
                print(f'Respuesta de la API: {response.json()}')
                messages.success(request, 'Categoria modificada correctamente')
                return redirect('categorias')
            
            except requests.exceptions.HTTPError as e:
                print('Error al modificar categoria ', e)
                try:
                    print('Detalles del error: ', e.response.json())  # Obtener más detalles del error
                except ValueError:
                    print('No se pudo obtener detalles del error en formato JSON')
                messages.error(request, 'Hubo un error')
                return redirect('categorias')

        data = {
            'categoria': categoria,
        }
        return render(request, 'app/crud_categorias/modificar.html', data)
    
    except requests.exceptions.HTTPError as e:
        print('Error al obtener categoria: ', e)
        return redirect('categorias')
    

@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def eliminar_categoria(request, id):
    headers = {'Authorization': settings.API_TOKEN}
    try:
        response = requests.delete(f'http://{settings.API_BASE_URL}/delete-categoria/{id}/', headers=headers)
        response.raise_for_status()
        messages.success(request, "Eliminado Correctamente")
        return redirect('categorias')
    
    except requests.exceptions.HTTPError as e:
        print('Error al eliminar categoria ', e)
        try:
            print('Detalles del error: ', e.response.json())
        except ValueError:
            print('No se pudo obtener detalles del error en formato JSON')
        messages.error(request, 'Hubo un error al eliminar')
        return redirect('categorias')
    

@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def finanzas(request):
    headers = {'Authorization': settings.API_TOKEN}
    page = request.GET.get('page', 1)

    try:
        response = requests.get(f'http://{settings.API_BASE_TRANSBANK_URL}/transactions', headers=headers)
        response.raise_for_status()
        transactions = response.json()

        try:
            paginator = Paginator(transactions, 5)
            transactions = paginator.page(page)
        except:
            raise Http404
        
        data = {
            'entity': transactions,
            'paginator': paginator,
        }
        return render(request, 'app/finanzas.html', data)
    except:
        messages.error(request, 'Error al obtener transacciones')
        return redirect('index')


@user_passes_test(lambda u: u.is_staff, login_url='admin_login')
def export_to_excel(request):
    headers = {'Authorization': settings.API_TOKEN}

    try:
        response = requests.get(f'http://{settings.API_BASE_TRANSBANK_URL}/transactions', headers=headers)
        response.raise_for_status()
        transactions = response.json()

        # Crear un libro de trabajo y una hoja de trabajo
        wb = Workbook()
        ws = wb.active
        ws.title = "Transacciones"

        # Añadir encabezados de columna
        ws.append(["ID", "Orden de compra", "Monto", "Estado", "Usuario asociado", "Fecha"])

        # Añadir datos de transacciones
        for transaction in transactions:
            ws.append([
                transaction.get('id'),
                transaction.get('buy_order'),
                transaction.get('amount'),
                transaction.get('status'),
                f"{transaction.get('user', {}).get('first_name', '')} {transaction.get('user', {}).get('last_name', '')}",
                transaction.get('transaction_date')
            ])

        # Configurar la respuesta para descargar el archivo Excel
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=transacciones.xlsx'
        wb.save(response)

        return response
    except:
        messages.error(request, 'Error al generar el archivo Excel')
        return redirect('finanzas')
    
    