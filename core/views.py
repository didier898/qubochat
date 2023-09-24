from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .forms import SignUpForm, UserProfileForm
from .models import Message, UserProfile, Conversation
from .serializers import MessageSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import json
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@csrf_exempt
def index(request):
    if request.user.is_authenticated:
        return redirect('edit_profile')
    if request.method == 'GET':
        return render(request, 'chat/index.html', {})
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile/edit/')  
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')  
            return HttpResponse('{"error": "User does not exist"}')

@login_required
def profile_view(request):
    user_profile = request.user
    context = {
        'user_profile': user_profile,
        'user_id': user_profile.id,  
    }
    return render(request, 'chat/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'chat/editar_perfil.html', {'form': form})

@login_required
def chat_conversacion(request, conversacion_id):
    
    conversacion = get_object_or_404(Conversation, id=conversacion_id)

    
    if request.user != conversacion.user1 and request.user != conversacion.user2:
        return render(request, 'chat/error.html', {'error_message': 'No tienes permiso para ver esta conversación.'})

    
    mensajes = Message.objects.filter(conversation=conversacion).order_by('fecha_envio')

    return render(request, 'chat/conversacion.html', {'conversacion': conversacion, 'mensajes': mensajes})

@login_required
def enviar_mensaje(request):
    if request.method == 'POST':
        
        receptor_id = request.POST.get('receptor_id')
        mensaje = request.POST.get('mensaje')

        try:
            
            receptor = UserProfile.objects.get(pk=receptor_id)

            
            conversacion, creada = Conversation.objects.get_or_create(
                user1=request.user,
                user2=receptor
            )

           
            Message.objects.create(
                sender=request.user,
                receiver=receptor,
                message=mensaje,
                conversation=conversacion
            )

            messages.success(request, 'Mensaje enviado exitosamente.')
            return redirect('chat')  

        except UserProfile.DoesNotExist:
            messages.error(request, 'El usuario con el ID proporcionado no existe.')
        except Exception as e:
            messages.error(request, f'Hubo un error al enviar el mensaje: {str(e)}')

    return render(request, 'chat/enviar_mensaje.html')

@login_required
def chat(request):
    # Obtener todas las conversaciones del usuario actual
    conversaciones = Conversation.objects.filter(user1=request.user) | Conversation.objects.filter(user2=request.user)

    # Obtener el ID de la conversación seleccionada de la URL
    conversacion_id = request.GET.get('conversacion_id')
    
    # Definir aquí la conversación seleccionada
    conversacion_seleccionada = None

    # Lista para almacenar los mensajes de la conversación seleccionada
    mensajes_de_conversacion = []

    if conversacion_id:
        # Obtener la conversación seleccionada por ID
        conversacion_seleccionada = get_object_or_404(Conversation, id=conversacion_id)

        # Obtener todos los mensajes de la conversación seleccionada
        mensajes_de_conversacion = Message.objects.filter(conversation=conversacion_seleccionada)

    return render(request, 'chat/chat.html', {
        'conversaciones': conversaciones,
        'mensajes_por_conversacion': mensajes_de_conversacion,
        'conversacion_seleccionada': conversacion_seleccionada,
    })
    
@csrf_exempt
@api_view(['GET', 'POST'])
def chat_api(request):
    # Obtener todas las conversaciones del usuario actual
    conversaciones = Conversation.objects.filter(user1=request.user) | Conversation.objects.filter(user2=request.user)
    
    # Definir aquí la conversación seleccionada (por ejemplo, la primera conversación)
    conversacion_seleccionada = None
    
    # Crear una lista para almacenar los datos de la conversación seleccionada
    datos_de_conversacion = []
    
    for conversacion in conversaciones:
        # Obtener el último mensaje en la conversación
        ultimo_mensaje = Message.objects.filter(conversation=conversacion).order_by('-timestamp').first()
        
        # Obtener el username del usuario que envió el último mensaje
        if ultimo_mensaje:
            username_del_enviador = ultimo_mensaje.sender.username
        else:
            # Manejar el caso en que no haya mensajes en la conversación
            username_del_enviador = None
        
        # Obtener los datos relevantes de la conversación
        datos = {
            'id': conversacion.id,
            'otro_usuario_id': conversacion.get_other_user(request.user).id,
            'ultimo_mensaje_enviado_por': username_del_enviador,
            
        }
        
        # Agregarlos a la lista de datos si es la conversación seleccionada
        if conversacion == conversacion_seleccionada:
            datos_de_conversacion.append(datos)

    # Serializar los datos en un formato JSON
    data = {
        'conversaciones': datos_de_conversacion,
        'conversacionSeleccionada': conversacion_seleccionada.id if conversacion_seleccionada else None,
    }

    return JsonResponse(data)

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # Verificar que las contraseñas coincidan
            if password != form.cleaned_data['password2']:
                messages.error(request, 'Las contraseñas no coinciden. Por favor, inténtalo de nuevo.')
                return redirect('register')

            # Obtener el valor del PIN del formulario
            pin = form.cleaned_data['pin']

            try:
                # Intentar crear el usuario
                user = UserProfile.objects.create_user(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)

                        # Crear el perfil con el PIN proporcionado
                        profile = UserProfile.objects.create(
                            pin=pin,
                            profile_picture=form.cleaned_data['profile_picture']
                        )

                        messages.success(request, 'Registro exitoso. ¡Bienvenido a QuboChat!')
                        return redirect('index')
            except IntegrityError:
                return redirect('index')

        else:
            print(form.errors)
            messages.error(request, 'Hubo un problema con el registro. Por favor, verifica tus datos.')

    else:
        form = SignUpForm()
    template = 'chat/register.html'
    context = {'form': form}
    return render(request, template, context)

@csrf_exempt
@api_view(['GET', 'POST'])
def register_api(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        form = SignUpForm(data)
        print(data)
        print(form)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # Verificar que las contraseñas coincidan
            if password != form.cleaned_data['password2']:
                response_data = {'error': 'Las contraseñas no coinciden. Por favor, inténtalo de nuevo.'}
                return JsonResponse(response_data, status=400)

            # Obtener el valor del PIN del formulario
            pin = form.cleaned_data['pin']

            try:
                
                user = UserProfile.objects.create_user(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)

                        # Crear el perfil con el PIN proporcionado
                        profile = UserProfile.objects.create(
                            pin=pin,
                            profile_picture=form.cleaned_data['profile_picture']
                        )

                        response_data = {'message': 'Registro exitoso. ¡Bienvenido a QuboChat!'}
                        print(f"Registro exitoso para usuario: {username}")
                        return JsonResponse(response_data)
            except IntegrityError as e:
                response_data = {'error': 'Hubo un problema con el registro. Por favor, verifica tus datos.'}
                print(f"Error en el registro: {e}")
                return JsonResponse(response_data, status=400)
        else:
            # Impresión de depuración para ver los errores de validación específicos del formulario
            print("Formulario no válido")
            print(form.errors)  

    else:
        response_data = {'error': 'Método no permitido'}
        return JsonResponse(response_data, status=405)
    
@csrf_exempt
@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def profilee_view(request):
    if request.user.is_authenticated:
        user_profile = request.user.userprofile  
        profile_data = {
            'user_id': user_profile.user.id,
            'pin': user_profile.pin,
            'profile_picture_url': user_profile.profile_picture.url,  
        }
        print(profile_data)
        return Response(profile_data)
    else:
        return Response({'error': 'Usuario no autenticado'}, status=401)


@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])  
def edit_profilee(request):
    if request.method == 'POST':
        try:
            
            data = json.loads(request.body.decode('utf-8-sig'))  

            
            user = request.user

            
            if 'username' in data:
                user.username = data['username']
            if 'pin' in data:
                user.userprofile.pin = data['pin']

            
            user.save()
            user.userprofile.save()

            return JsonResponse({'message': 'Perfil actualizado con éxito'})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Error en los datos JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

@api_view(['GET', 'POST'])
def lista_mensajes(request):
    if request.method == 'GET':
        mensajes = Message.objects.all()
        serializer = MessageSerializer(mensajes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def detalle_mensaje(request, mensaje_id):
    try:
        mensaje = Message.objects.get(pk=mensaje_id)
    except Message.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MessageSerializer(mensaje)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MessageSerializer(mensaje, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        mensaje.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@csrf_exempt
@api_view(['GET', 'POST'])    
def login_and_return_json(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8-sig'))
            username = data.get("username")
            password = data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None and user.is_active:
                login(request, user)

                
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                
                print(f"Token JWT generado para el usuario {user.username}:")
                print(f"  User ID: {user.id}")
                print(f"  Username: {user.username}")
                print(f"  Access Token: {access_token}")

                
                response_data = {
                    "success": True,
                    "message": "Inicio de sesión exitoso",
                    "user_id": user.id,
                    "username": user.username,
                    "access_token": access_token,  
                }
                return JsonResponse(response_data)
            else:
                return JsonResponse({"error": "Credenciales incorrectas"}, status=400)
        except json.JSONDecodeError as e:
            return JsonResponse({"error": "Error en los datos JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)
 
      
def usuario_autenticado(request):
    if request.user.is_authenticated:
        
        return JsonResponse({"usuario_autenticado": True})
    else:
        
        return JsonResponse({"usuario_autenticado": False})
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def apichat_conversacion(request, conversacion_id):
    
    conversacion = get_object_or_404(Conversation, id=conversacion_id)

    
    if request.user != conversacion.user1 and request.user != conversacion.user2:
        return JsonResponse({'error': 'No tienes permiso para ver esta conversación.'}, status=403)

    
    mensajes = Message.objects.filter(conversation=conversacion).order_by('fecha_envio')

    
    mensajes_json = [{'sender': mensaje.sender.username, 'message': mensaje.message} for mensaje in mensajes]

    
    data = {
        'conversacion_id': conversacion.id,
        'mensajes': mensajes_json,
    }

    
    return JsonResponse(data)