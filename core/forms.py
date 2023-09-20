from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from django.contrib.auth import get_user_model

class SignUpForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    pin = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    
    # Agregar la validación de unicidad para el campo 'username'
    #username = forms.CharField(
        #widget=forms.TextInput(attrs={'class': 'form-control'}),
        #help_text="Este campo es requerido. 150 caracteres o menos. Letras, dígitos y @ /. / - / _ solamente.",
    #)

    class Meta:
        model = get_user_model()  # Utiliza esta función para obtener el modelo de usuario actual
        fields = ['username', 'password1', 'password2', 'pin', 'profile_picture']
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['pin','profile_picture']
        widgets = {
            'pin': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

