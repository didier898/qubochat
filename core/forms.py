from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

class SignUpForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    pin = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    profile_picture = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        required=False,  # Agregar esta línea para hacer el campo opcional
    )

    class Meta:
        model = get_user_model()  
        fields = ['username', 'password1', 'password2', 'pin', 'profile_picture']
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['pin','profile_picture']
        widgets = {
            'pin': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

