from django.urls import path
from . import views

urlpatterns = [
   path('', views.index, name='home'),
   path('detalle-producto/<str:id>/', views.detalle_producto, name='detalle_producto'),
   path('checkout/', views.checkout, name='checkout'),
   path('agregar-carrito/<str:id>/', views.agregar_carrito, name='agregar-carrito'),
   path('restar-carrito/<str:id>/', views.restar_carrito, name='restar-carrito'),
   path('eliminar-carrito/<str:id>/', views.eliminar_carrito, name='eliminar-carrito'),
   path('limpiar-carrito/', views.limpiar_carrito, name='limpiar-carrito'),
]