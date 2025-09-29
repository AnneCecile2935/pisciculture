from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Adresse email")

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2')
        label = {
            'email': 'Adresse e-mail',
            'fisrt_name': 'Prénom',
            'last_name': 'Nom',
            'username': "Nom d'utilisateur",
            'password1': 'Mot de passe',
            'password2': 'Confirmation du mot de passe',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
