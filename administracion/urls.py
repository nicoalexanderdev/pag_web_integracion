from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('home', views.index, name='index'),
    path('productos', views.listar_productos, name='productos'),
    path('productos/agregar', views.agregar_producto, name='agregar_producto'),
    path('productos/modificar/<int:id>', views.modificar_producto, name='modificar_producto'),
    path('productos/eliminar/<int:id>', views.eliminar_producto, name='eliminar_productos'),
    path('marcas', views.listar_marcas, name='marcas'),
    path('marcas/agregar', views.agregar_marca, name='agregar_marca'),
    path('marcas/modificar/<int:id>', views.modificar_marca, name='modificar_marca'),
    path('marcas/eliminar/<int:id>', views.eliminar_marca, name='eliminar_marca'),
    path('categorias', views.listar_categorias, name='categorias'),
    path('categorias/agregar', views.agregar_categoria, name='agregar_categoria'),
    path('categorias/modificar/<int:id>', views.modificar_categoria, name='modificar_categoria'),
    path('categorias/eliminar/<int:id>', views.eliminar_categoria, name='eliminar_categoria'),
]
