from django.urls import path
from . import views

urlpatterns = [
   path('', views.index, name='home'),
   path('detalle-producto/<str:id>/', views.detalle_producto, name='detalle_producto'),
]