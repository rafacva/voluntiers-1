from django import forms
from utils.django_forms import add_placeholder


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['Usuário'], 'Digite seu nome de usuário')
        add_placeholder(self.fields['Senha'], 'Digite sua senha')

    Usuário = forms.CharField()
    Senha = forms.CharField(
        widget=forms.PasswordInput()
    )
