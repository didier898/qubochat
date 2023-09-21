from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import SignUpForm, UserProfileForm
from django.contrib import messages
from django.db import IntegrityError
from .models import Message, UserProfile
from .models import Conversation
from django.shortcuts import render, get_object_or_404
 


def index(request):
    if request.user.is_authenticated:
        return redirect('edit_profile')
    if request.method == 'GET':
        return render(request, 'chat/index.html', {})
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirige al usuario a 'index' después de iniciar sesión
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')  # Mensaje de error
            return HttpResponse('{"error": "User does not exist"}')


@login_required
def profile_view(request):
    user_profile = request.user
    context = {
        'user_profile': user_profile,
        'user_id': user_profile.id,  # Obtén el ID del usuario
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

def chat_conversacion(request, conversacion_id):
    # Obtener la conversación específica o mostrar un error 404 si no existe
    conversacion = get_object_or_404(Conversation, id=conversacion_id)

    # Verificar si el usuario actual está autorizado para ver esta conversación
    if request.user != conversacion.user1 and request.user != conversacion.user2:
        return render(request, 'chat/error.html', {'error_message': 'No tienes permiso para ver esta conversación.'})

    # Obtener todos los mensajes de la conversación
    mensajes = Message.objects.filter(conversation=conversacion).order_by('fecha_envio')

    return render(request, 'chat/conversacion.html', {'conversacion': conversacion, 'mensajes': mensajes})

@login_required
def enviar_mensaje(request):
    if request.method == 'POST':
        # Obtener el ID del receptor y el contenido del mensaje del formulario
        receptor_id = request.POST.get('receptor_id')
        mensaje = request.POST.get('mensaje')

        try:
            # Verificar si el usuario receptor existe
            receptor = UserProfile.objects.get(pk=receptor_id)

            # Verificar si ya existe una conversación entre el usuario actual y el receptor
            conversacion, creada = Conversation.objects.get_or_create(
                user1=request.user,
                user2=receptor
            )

            # Crear el mensaje en la conversación
            Message.objects.create(
                sender=request.user,
                receiver=receptor,
                message=mensaje,
                conversation=conversacion
            )

            messages.success(request, 'Mensaje enviado exitosamente.')
            return redirect('chat')  # Redirige al usuario a la página de chat después de enviar el mensaje

        except UserProfile.DoesNotExist:
            messages.error(request, 'El usuario con el ID proporcionado no existe.')
        except Exception as e:
            messages.error(request, f'Hubo un error al enviar el mensaje: {str(e)}')

    return render(request, 'chat/enviar_mensaje.html')

@login_required
def chat(request):
    # Obtener todas las conversaciones del usuario actual
    conversaciones = Conversation.objects.filter(user1=request.user) | Conversation.objects.filter(user2=request.user)
    
    # Definir aquí la conversación seleccionada (por ejemplo, la primera conversación)
    conversacion_seleccionada = None
    
    # Crear una lista para almacenar los mensajes de la conversación seleccionada
    mensajes_de_conversacion = []
    
    for conversacion in conversaciones:
        # Obtener los mensajes para esta conversación
        mensajes = Message.objects.filter(conversation=conversacion)
        
        # Agregarlos a la lista de mensajes si es la conversación seleccionada
        if conversacion == conversacion_seleccionada:
            mensajes_de_conversacion.extend(mensajes)

    return render(request, 'chat/chat.html', {
        'conversaciones': conversaciones,
        'mensajes_por_conversacion': mensajes_de_conversacion,  # Cambiar el nombre de la variable
        'conversacion_seleccionada': conversacion_seleccionada,
    })




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


