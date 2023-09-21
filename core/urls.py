from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
#from django.conf import settings
#from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('enviar-mensaje/', views.enviar_mensaje, name='enviar_mensaje'),
    path('chat/', views.chat, name='chat'),  # Agrega esta línea
    path('chat/<int:conversacion_id>/', views.chat_conversacion, name='chat_conversacion'),

]

#if settings.DEBUG:
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
