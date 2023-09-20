from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chats/', views.chat_view, name='chats'),  # Cambiado de 'chat/chats/' a 'chats/'
    path('chats/<int:sender>/<int:receiver>/', views.message_view, name='message'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
