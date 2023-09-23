from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from django.contrib import admin
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('enviar-mensaje/', views.enviar_mensaje, name='enviar_mensaje'),
    path('chat/', views.chat, name='chat'),  
    path('chat/<int:conversacion_id>/', views.chat_conversacion, name='chat_conversacion'),
    path('admin/', admin.site.urls),
    path('api/registro/', views.register_api, name='registro_api'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('api/profilee/', views.profilee_view, name='profile_api'),
    path('api/editar_perfilee/', views.edit_profilee, name='editar_perfil'),
    path('api/mensajes/', views.lista_mensajes, name='lista_mensajes'),
    path('api/mensajes/<int:mensaje_id>/', views.detalle_mensaje, name='detalle_mensaje'),
    path('login/', views.login_view, name='login_view'),
    path('api/usuario_autenticado/', views.usuario_autenticado, name='usuario_autenticado'),
    path('api/chat_conversacion/', views.apichat_conversacion, name='apichat_conversacion'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
