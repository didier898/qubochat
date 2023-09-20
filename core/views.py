from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import SignUpForm, UserProfileForm
from django.contrib import messages
from django.db import IntegrityError
from .models import Message, UserProfile
from .models import Conversation
 


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

    return render(request, 'chat/chat.html', {'conversaciones': conversaciones})



@login_required
def chat_conversacion(request, conversacion_id):
    try:
        conversacion = Conversation.objects.get(pk=conversacion_id)

        # Verificar si el usuario actual es parte de la conversación
        if request.user in (conversacion.user1, conversacion.user2):
            mensajes = Message.objects.filter(conversation=conversacion)

            if request.method == 'POST':
                # Procesar el envío de un nuevo mensaje en la conversación
                mensaje = request.POST.get('mensaje')
                # Determinar quién es el receptor en función del usuario actual
                receptor = conversacion.user1 if request.user == conversacion.user2 else conversacion.user2
                Message.objects.create(
                    sender=request.user,
                    receiver=receptor,
                    message=mensaje,
                    conversation=conversacion
                )

            return render(request, 'chat/conversacion.html', {'conversacion': conversacion, 'mensajes': mensajes})

        else:
            # Manejar el caso en el que la conversación no pertenece al usuario
            messages.error(request, 'No tienes acceso a esta conversación.')
            return redirect('chat')

    except Conversation.DoesNotExist:
        # Manejar el caso en el que la conversación no existe
        messages.error(request, 'La conversación no existe.')
        return redirect('chat')


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


