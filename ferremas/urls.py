from django.urls import path
from . import views

urlpatterns = [
   path('', views.index, name='home'),
   path('detalle-producto/<str:id>/', views.detalle_producto, name='detalle_producto'),
   path('checkout/', views.checkout, name='checkout'),
   path('agregar-carrito/<int:id>/', views.agregar_carrito, name='agregar-carrito'),
   path('restar-carrito/<int:id>/', views.restar_carrito, name='restar-carrito'),
   path('eliminar-carrito/<str:id>/', views.eliminar_carrito, name='eliminar-carrito'),
   path('limpiar-carrito/', views.limpiar_carrito, name='limpiar-carrito'),
   path('ir-a-pagar/', views.ir_a_pagar, name='ir-a-pagar'),
   path('transbank/', views.transbank, name='transbank'),
   path('categoria/<str:id>', views.categoria, name='categoria'),
   path('marca/<str:id>', views.marca, name='marca'),
   path('registro/', views.registro, name='registro'),
   path('agregar-direccion/', views.agregar_direccion, name='agregar_direccion'),
   path('detalles-entrega/', views.agregar_detalles_entrega, name='agregar_detalles_entrega'),
   path('pago/', views.pago, name='pago'),
]