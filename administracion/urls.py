from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('home', views.index, name='index'),
    path('productos', views.listar_productos, name='productos'),
    path('productos/agregar', views.agregar_producto, name='agregar_producto'),
    path('productos/modificar/<int:id>', views.modificar_producto, name='modificar_producto'),
    path('productos/eliminar/<int:id>', views.eliminar_producto, name='eliminar_productos'),
]
