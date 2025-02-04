"""
URL configuration for event_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from events import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('eventos/', views.lista_eventos, name='lista_eventos'),
    path('eventos/crear/', views.crear_evento, name='crear_evento'),
    path('eventos/detalle/<int:evento_id>/', views.detalle_evento, name='detalle_evento'),
    path('eventos/actualizar/<int:evento_id>/', views.actualizar_evento, name='actualizar_evento'),
    path('eventos/eliminar/<int:evento_id>/', views.eliminar_evento, name='eliminar_evento'),
    path('reservas/<int:usuario_id>/', views.gestionar_reservas, name='listar_reservas'),
    path('reservas/<int:usuario_id>/<int:reserva_id>/', views.gestionar_reservas, name='gestionar_reserva'),
    path('comentarios/<int:evento_id>/', views.gestionar_comentarios, name='listar_comentarios'),
    path('comentarios/<int:evento_id>/<int:usuario_id>/', views.gestionar_comentarios, name='crear_comentario'),
    path('usuario/register/', views.registrar_usuario, name='registrar_usuario'),
    path('usuario/login/', views.login_usuario, name='login_usuario'),
]