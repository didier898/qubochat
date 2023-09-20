from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import SignUpForm, UserProfileForm
from .models import Message, UserProfile
from django.contrib import messages
import random

def index(request):
    if request.user.is_authenticated:
        return redirect('chats')
    if request.method == 'GET':
        return render(request, 'chat/index.html', {})
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
            return HttpResponse('{"error": "User does not exist"}')

@login_required
def chat_view(request):
    if request.method == "GET":
        return render(request, 'chat/chats.html',
                      {'users': UserProfile.objects.exclude(username=request.user.username)})

@login_required
def message_view(request, sender, receiver):
    if request.method == "GET":
        sender_profile = UserProfile.objects.get(id=sender)
        receiver_profile = UserProfile.objects.get(id=receiver)
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver) | \
                   Message.objects.filter(sender_id=receiver, receiver_id=sender)
        
        context = {
            'users': {'sender': sender_profile, 'receiver': receiver_profile},
            'messages': messages,
        }

        return render(request, "chat/messages.html", context)


@login_required
def profile_view(request):
    user_profile = request.user  # Accede al perfil del usuario directamente
    context = {
        'user_profile': user_profile,
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

            # Generar automáticamente un PIN único para el usuario
            while True:
                pin = ''.join(random.choices('0123456789', k=10))
                if not UserProfile.objects.filter(pin=pin).exists():
                    break

            # Crear el usuario con el PIN generado
            user = UserProfile.objects.create_user(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)

                    profile = UserProfile.objects.create(pin=pin, profile_picture=form.cleaned_data['profile_picture'])

                    messages.success(request, 'Registro exitoso. ¡Bienvenido a QuboChat!')
                    return redirect('index')
        else:
            print(form.errors)
            messages.error(request, 'Hubo un problema con el registro. Por favor, verifica tus datos.')

    else:
        form = SignUpForm()
    template = 'chat/register.html'
    context = {'form': form}
    return render(request, template, context)
