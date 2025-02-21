from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.middleware.csrf import get_token
import json
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import User, Event, Reservation, Comment
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

#CRUD DE EVENTOS:

#lista de eventos
@csrf_exempt
def lista_eventos(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    #Obtener parámetros de la solicitud
    title_filter = request.GET.get('title', '').strip() #con strip eliminamos los espacios en blanco, así dan menos errores al introducir datos
    date_filter = request.GET.get('date', '').strip()
    order_by = request.GET.get('order_by', 'date_time') #por defecto, ordenar por fecha
    page = request.GET.get('page', 1)

    #filtrar eventos
    eventos = Event.objects.all()

    if title_filter:
        eventos = eventos.filter(title__icontains=title_filter) #__icontains es un look-up field de Django que realiza una búsqueda insensible (case-insensitive) y verifica si un valor está contenido en el campo title.
        #básicamente busca si el valor de title_filter (lo que el usuario está buscando) aparece en algún lugar dentro del campo title, sin importar si son mayúsculas o minúsculas

    if date_filter:
        eventos = eventos.filter(date_time__date=date_filter) #filtrar por fecha exacta

    #ordenar eventos
    if order_by in ['title', '-title', 'date_time', '-date_time', 'capacity', '-capacity']: #order_by es el parámetro que el usuario envía en la URL (query string) para especificar cómo quiere ordenar los eventos
        #(GET /eventos/?order_by=title, así se ordenan los eventos por orden ascendente). El prefijo - indica un orden descendente. Sin el prefijo, ordena en orden ascendente
        #de este modo, si el valor de order_by es válido(es decir, está en la lista), aplicamos la ordenación usando el método order_by y Django generará la consulta SQL correspondiente, algo como: SELECT * FROM events ORDER BY date_time ASC;
        eventos = eventos.order_by(order_by)

    #paginar eventos(5 por página)
    paginator = Paginator(eventos, 5)

    try:
        eventos_pagina = paginator.page(page)
    except:
        return JsonResponse({'error': 'Página fuera de rango'}, status=400)
    
    #convertimos a JSON
    eventos_json = list(eventos_pagina.object_list.values('id', 'title', 'description', 'date_time', 'capacity', 'image_url', 'organizer__username'))

    return JsonResponse({
        'total': paginator.count,
        'pages': paginator.num_pages,
        'current_page': eventos_pagina.number,
        'next_page': eventos_pagina.next_page_number() if eventos_pagina.has_next() else None,
        'prev_page': eventos_pagina.previous_page_number() if eventos_pagina.has_previous() else None,
        'eventos': eventos_json
    }, safe=False)

#crear un evento
@csrf_exempt
def crear_evento(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            title = data['title']
            description = data['description']
            date_time = data['date_time']
            capacity = int(data['capacity']) #convertimos a entero
            organizer_id = int(data['organizer']) #convertimos a entero
            image_url = data.get('image_url', None)

            #aquí buscamos al organizador y validamos que es organizer
            try:
                organizer = User.objects.get(id=organizer_id, role='organizer')
            except User.DoesNotExist:
                return JsonResponse({'error': 'Organizador no encontrado o no es un organizador'}, status=404)

            #aquí creamos el evento solo si el organizador es válido
            evento = Event.objects.create(
                title=title,
                description=description,
                date_time=date_time,
                capacity=capacity,
                image_url=image_url,
                organizer=organizer
            )

            return JsonResponse({'message': 'Evento creado con éxito', 'evento_id': evento.id}, status=201)
        
        except KeyError as e:
            return JsonResponse({'error': f'Falta el parámetro requerido: {str(e)}'}, status=400)
        
        except ValueError:
            return JsonResponse({'error': 'Formato inválido en capacidad u organizador'}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'El cuerpo de la solicitud debe ser JSON válido'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

#ver detalles de un evento
def detalle_evento(request, evento_id):
    try:
        evento = Event.objects.get(id=evento_id)
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Evento no encontrado'}, status=404)
    
    data = {
        'id': evento.id,
        'title': evento.title,
        'description': evento.description,
        'date_time': evento.date_time,
        'capacity': evento.capacity,
        'image_url': evento.image_url,
        'organizer': evento.organizer.username
    }
    return JsonResponse(data, safe=False)

#actualizar un evento
@csrf_exempt
def actualizar_evento(request, evento_id):
    if request.method not in ['PUT', 'PATCH']:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        evento = Event.objects.get(id=evento_id)
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Evento no encontrado'}, status=404)
    
    try:
        data = json.loads(request.body.decode('utf-8'))

        #solo tomamos los valores si están en la petición
        if request.method =='PUT':
            #en 'PUT', todos los campos son obligatorios
            evento.title = data['title']
            evento.description = data['description']
            evento.date_time = data['date_time']
            evento.capacity = int(data['capacity'])
            evento.image_url = data.get['image_url', evento.image_url]
        elif request.method == 'PATCH':
            #en 'PATCH', solo actualizamos los campos enviados
            if 'title' in data:
                evento.title = data['title']
            if 'description' in data:
                evento.description = data['description']
            if 'date_time' in data:
                evento.date_time = data['date_time']
            if 'capacity' in data:
                evento.capacity = int(data['capacity'])
            if 'image_url' in data:
                evento.image_url = data['image_url']

    except KeyError as e:
        return JsonResponse({'error': f'Falta el parámetro requerido: {str(e)}'}, status=400)
    
    except ValueError:
        return JsonResponse({'error': 'El campo "capacity" debe ser un número entero válido'}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'El cuerpo de la solicitud debe ser JSON válido'}, status=400)

    evento.save()
    return JsonResponse({'message': 'Evento actualizado con éxito'})

#eliminar un evento
@csrf_exempt
def eliminar_evento(request, evento_id):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        evento = Event.objects.get(id=evento_id)
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Evento no encontrado'}, status=404)

    evento.delete()
    return JsonResponse({'message': 'Evento eliminado con éxito'}, status=200)


#GESTIÓN DE RESERVAS:

@csrf_exempt
def gestionar_reservas(request, usuario_id, reserva_id=None):
    """Gestión de reservas: GET (listar), POST (crear), PUT/PATCH (actualizar estado), DELETE (cancelar)"""
    
    #Obtener usuario autenticado
    try:
        usuario = User.objects.get(id=usuario_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

    #GET: Listar reservas de un usuario autenticado
    if request.method == 'GET':
        reservas = Reservation.objects.filter(user=usuario)
        reservas_json = list(reservas.values('id', 'event__title', 'tickets', 'status'))
        return JsonResponse({'reservas': reservas_json}, safe=False)

    #POST: Crear una nueva reserva
    elif request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            event_id = data['event_id']
            tickets = int(data['tickets'])

            #Validar que el evento existe
            try:
                evento = Event.objects.get(id=event_id)
            except Event.DoesNotExist:
                return JsonResponse({'error': 'Evento no encontrado'}, status=404)

            #Validar que hay suficiente capacidad en el evento
            total_reservados = sum(res.tickets for res in evento.reservations.all())
            if total_reservados + tickets > evento.capacity:
                return JsonResponse({'error': 'No hay suficientes plazas disponibles'}, status=400)

            #Crear reserva
            reserva = Reservation.objects.create(user=usuario, event=evento, tickets=tickets)
            return JsonResponse({'message': 'Reserva creada con éxito', 'reserva_id': reserva.id}, status=201)

        except KeyError as e:
            return JsonResponse({'error': f'Falta el parámetro requerido: {str(e)}'}, status=400)
        
        except ValueError:
            return JsonResponse({'error': 'Formato inválido en tickets'}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'El cuerpo de la solicitud debe ser JSON válido'}, status=400)

    #PUT/PATCH: Actualizar el estado de una reserva (solo organizadores)
    elif request.method in ['PUT', 'PATCH']:
        if not reserva_id:
            return JsonResponse({'error': 'Se requiere un ID de reserva para actualizar'}, status=400)

        try:
            reserva = Reservation.objects.get(id=reserva_id)
        except Reservation.DoesNotExist:
            return JsonResponse({'error': 'Reserva no encontrada'}, status=404)

        #Solo organizadores pueden cambiar el estado de una reserva
        if usuario.role != 'organizer':
            return JsonResponse({'error': 'No tienes permisos para modificar reservas'}, status=403)

        try:
            data = json.loads(request.body.decode('utf-8'))
            if 'status' in data:
                if data['status'] not in ['pending', 'confirmed', 'cancelled']:
                    return JsonResponse({'error': 'Estado de reserva inválido'}, status=400)
                reserva.status = data['status']

            reserva.save()
            return JsonResponse({'message': 'Reserva actualizada con éxito'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'El cuerpo de la solicitud debe ser JSON válido'}, status=400)

    #DELETE: Cancelar una reserva (solo participantes para sus reservas)
    elif request.method == 'DELETE':
        if not reserva_id:
            return JsonResponse({'error': 'Se requiere un ID de reserva para cancelar'}, status=400)

        try:
            reserva = Reservation.objects.get(id=reserva_id, user=usuario)
        except Reservation.DoesNotExist:
            return JsonResponse({'error': 'Reserva no encontrada o no pertenece al usuario'}, status=404)

        reserva.delete()
        
        return JsonResponse({'message': 'Reserva cancelada con éxito'}, status=200)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def gestionar_comentarios(request, evento_id, usuario_id=None):
    """Gestión de comentarios: GET (listar), POST (crear)"""
    
    #GET: Listar comentarios de un evento
    if request.method == 'GET':
        try:
            evento = Event.objects.get(id=evento_id)
        except Event.DoesNotExist:
            return JsonResponse({'error': 'Evento no encontrado'}, status=404)

        comentarios = Comment.objects.filter(event=evento).order_by('-created_at')
        comentarios_json = list(comentarios.values('id', 'user__username', 'text', 'created_at'))
        return JsonResponse({'comentarios': comentarios_json}, safe=False)

    #POST: Crear un comentario asociado a un evento (solo usuarios autenticados)
    elif request.method == 'POST':
        if not usuario_id:
            return JsonResponse({'error': 'Se requiere un usuario autenticado para comentar'}, status=400)

        try:
            usuario = User.objects.get(id=usuario_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

        try:
            evento = Event.objects.get(id=evento_id)
        except Event.DoesNotExist:
            return JsonResponse({'error': 'Evento no encontrado'}, status=404)

        try:
            data = json.loads(request.body.decode('utf-8'))
            texto = data['text'].strip()

            if not texto:
                return JsonResponse({'error': 'El comentario no puede estar vacío'}, status=400)

            #Crear el comentario
            comentario = Comment.objects.create(user=usuario, event=evento, text=texto)

            return JsonResponse({'message': 'Comentario añadido con éxito', 'comentario_id': comentario.id}, status=201)

        except KeyError as e:
            return JsonResponse({'error': f'Falta el parámetro requerido: {str(e)}'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'El cuerpo de la solicitud debe ser JSON válido'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def registrar_usuario(request):
    """Registro de nuevos usuarios"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data['username'].strip()
        password = data['password']
        role = data.get('role', 'participant')  #Por defecto, 'participant'
        biography = data.get('biography', '')

        #Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'El nombre de usuario ya está en uso'}, status=400)

        #Crear usuario
        user = User.objects.create(
            username=username,
            password=make_password(password),  #Hashear la contraseña
            role=role,
            biography=biography
        )

        return JsonResponse({'message': 'Usuario registrado con éxito', 'user_id': user.id}, status=201)

    except KeyError as e:
        return JsonResponse({'error': f'Falta el parámetro requerido: {str(e)}'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'El cuerpo de la solicitud debe ser JSON válido'}, status=400)


@csrf_exempt
def login_usuario(request):
    """Inicio de sesión de usuarios"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data['username'].strip()
        password = data['password']

        #Autenticar usuario
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'error': 'Credenciales inválidas'}, status=401)

        #Iniciar sesión
        login(request, user)

        return JsonResponse({'message': 'Inicio de sesión exitoso', 'user_id': user.id, 'role': user.role, 'csrf_token': get_token(request)}, status=200)

    except KeyError as e:
        return JsonResponse({'error': f'Falta el parámetro requerido: {str(e)}'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'El cuerpo de la solicitud debe ser JSON válido'}, status=400)
    

#Vamos a usar APIView para manejar autenticación con tokens.
class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format='password'),
                'role': openapi.Schema(type=openapi.TYPE_STRING, enum=['organizer', 'participant']),
                'biography': openapi.Schema(type=openapi.TYPE_STRING)
            },
            required=['username', 'password']
        ),
        responses={201: "Usuario creado exitosamente", 400: "Error en los datos"}
    )
    def post(self, request):
        data = request.data
        if User.objects.filter(username=data['username']).exists():
            return Response({'error': 'El usuario ya existe'}, status=400)

        user = User.objects.create(
            username=data['username'],
            password=make_password(data['password']),
            role=data.get('role', 'participant'),
            biography=data.get('biography', '')
        )

        token, created = Token.objects.get_or_create(user=user)

        return Response({'message': 'Usuario registrado con éxito', 'token': token.key}, status=201)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format='password'),
            },
            required=['username', 'password']
        ),
        responses={200: "Inicio de sesión exitoso", 401: "Credenciales inválidas"}
    )
    def post(self, request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if not user:
            return Response({'error': 'Credenciales inválidas'}, status=401)

        token, created = Token.objects.get_or_create(user=user)
        return Response({'message': 'Inicio de sesión exitoso', 'token': token.key})
    

#Solo los organizadores pueden crear, actualizar y eliminar eventos.
class ListaEventosAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        eventos = Event.objects.all().values('id', 'title', 'description', 'date_time', 'capacity', 'image_url', 'organizer__username')
        return Response({'eventos': list(eventos)})

class CrearEventoAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'organizer':
            return Response({'error': 'No tienes permisos para crear eventos'}, status=403)

        data = request.data
        evento = Event.objects.create(
            title=data['title'],
            description=data['description'],
            date_time=data['date_time'],
            capacity=data['capacity'],
            image_url=data.get('image_url', None),
            organizer=request.user
        )
        return Response({'message': 'Evento creado con éxito', 'evento_id': evento.id}, status=201)

class DetalleEventoAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, evento_id):
        try:
            evento = Event.objects.get(id=evento_id)
            return Response({
                'id': evento.id,
                'title': evento.title,
                'description': evento.description,
                'date_time': evento.date_time,
                'capacity': evento.capacity,
                'image_url': evento.image_url,
                'organizer': evento.organizer.username
            })
        except Event.DoesNotExist:
            return Response({'error': 'Evento no encontrado'}, status=404)



#Los participantes pueden crear y cancelar sus reservas, pero solo los organizadores pueden modificar estados.
class CrearReservaAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'participant':
            return Response({'error': 'No tienes permisos para hacer reservas'}, status=403)

        data = request.data
        try:
            evento = Event.objects.get(id=data['event_id'])
        except Event.DoesNotExist:
            return Response({'error': 'Evento no encontrado'}, status=404)

        reserva = Reservation.objects.create(
            user=request.user,
            event=evento,
            tickets=data['tickets']
        )
        return Response({'message': 'Reserva creada con éxito', 'reserva_id': reserva.id}, status=201)

class CancelarReservaAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, reserva_id):
        try:
            reserva = Reservation.objects.get(id=reserva_id, user=request.user)
        except Reservation.DoesNotExist:
            return Response({'error': 'Reserva no encontrada'}, status=404)

        reserva.delete()
        return Response({'message': 'Reserva cancelada con éxito'}, status=200)


