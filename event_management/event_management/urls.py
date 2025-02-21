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
from events.views import inicio, detalle_evento, panel_usuario
from rest_framework.authtoken.views import ObtainAuthToken
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from events import views
from rest_framework.permissions import AllowAny

from events.views import (
    ListaEventosAPIView, CrearEventoAPIView, DetalleEventoAPIView,
    CrearReservaAPIView, CancelarReservaAPIView, RegisterView, LoginView
)

schema_view = get_schema_view(
    openapi.Info(
        title="API de Gestión de Eventos",
        default_version="v1",
        description="Documentación de la API para gestionar eventos y reservas",
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    #Vistas con plantillas HTML (nuevas rutas)
    path('', inicio, name='inicio'),
    path('evento/<int:evento_id>/', detalle_evento, name='detalle_evento'), #buscamos el evento de id 3 por ejemplo
    path('panel/', panel_usuario, name='panel_usuario'),

    #Autenticación
    path('usuario/register/', RegisterView.as_view(), name='registrar_usuario'),
    path('usuario/login/', LoginView.as_view(), name='login_usuario'),
    path('api-token-auth/', ObtainAuthToken.as_view(), name='api_token_auth'),

    #Eventos (solo APIView)
    path('api/eventos/', ListaEventosAPIView.as_view(), name='lista_eventos'),
    path('api/eventos/crear/', CrearEventoAPIView.as_view(), name='crear_evento'),
    path('api/eventos/detalle/<int:evento_id>/', DetalleEventoAPIView.as_view(), name='detalle_evento'),

    #Reservas (solo APIView)
    path('api/reservas/crear/', CrearReservaAPIView.as_view(), name='crear_reserva'),
    path('api/reservas/cancelar/<int:reserva_id>/', CancelarReservaAPIView.as_view(), name='cancelar_reserva'),

    #Endpoints de documentación Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


"""
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


    #Modificamos urls.py para incluir las rutas con APIView.
    # Endpoints de autenticación
    path('usuario/register/', RegisterView.as_view(), name='registrar_usuario'),
    path('usuario/login/', LoginView.as_view(), name='login_usuario'),
    path('api-token-auth/', ObtainAuthToken.as_view(), name='api_token_auth'),

    # Endpoints de eventos
    path('eventos/', ListaEventosAPIView.as_view(), name='lista_eventos'),
    path('eventos/crear/', CrearEventoAPIView.as_view(), name='crear_evento'),
    path('eventos/detalle/<int:evento_id>/', DetalleEventoAPIView.as_view(), name='detalle_evento'),

    # Endpoints de reservas
    path('reservas/crear/', CrearReservaAPIView.as_view(), name='crear_reserva'),
    path('reservas/cancelar/<int:reserva_id>/', CancelarReservaAPIView.as_view(), name='cancelar_reserva'),
]
"""



"""
Cambio que he hecho en la etapa 4, he añadido arriba a estas url api/ para diferenciarlas mejor y tenga una estructura clara

#Eventos (solo APIView)
    path('eventos/', ListaEventosAPIView.as_view(), name='lista_eventos'),
    path('eventos/crear/', CrearEventoAPIView.as_view(), name='crear_evento'),
    path('eventos/detalle/<int:evento_id>/', DetalleEventoAPIView.as_view(), name='detalle_evento'),

    #Reservas (solo APIView)
    path('reservas/crear/', CrearReservaAPIView.as_view(), name='crear_reserva'),
    path('reservas/cancelar/<int:reserva_id>/', CancelarReservaAPIView.as_view(), name='cancelar_reserva'),

"""