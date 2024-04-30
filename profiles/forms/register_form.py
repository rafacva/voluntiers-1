from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import add_placeholder, strong_password


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['user_type'], 'ONG ou Voluntário')
        add_placeholder(self.fields['username'], 'Nome de Usuário')
        add_placeholder(self.fields['email'], 'E-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        add_placeholder(self.fields['password'], 'Digite sua senha')
        add_placeholder(self.fields['password2'], 'Repita sua senha')

    user_type = forms.ChoiceField(
    choices=[
        ('ONG', 'ONG'),
        ('Voluntier', 'Voluntier'),
        
    ],
    error_messages={'required': 'Please select an option'},
    label='Tipo de Usuário'
    )
    username = forms.CharField(
        label='Usuário',
        help_text=(
            'Nome de usuário deve conter letras, números ou um desses: @.+-_. '
            'O nome de usuário deve conter de 4 a 150 caracteres.'
        ),
        error_messages={
            'required': 'Este campo não pode ser vazio.',
            'min_length': 'Nome de usuário deve conter no mínimo 4 caracteres',
            'max_length': 'Nome de usuário deve conter menos de 150 caracteres',
        },
        min_length=4, max_length=150,
    )
    first_name = forms.CharField(
        error_messages={'required': 'Escreva seu nome'},
        label='Nome'
    )
    last_name = forms.CharField(
        error_messages={'required': 'Escreva seu sobrenome'},
        label='Sobrenome'
    )
    email = forms.EmailField(
        error_messages={'required': 'E-mail é necessário'},
        label='E-mail',
        help_text='O e-mail deve ser válido.',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Senha não pode ser vazia'
        },
        help_text=(
            'Senha deve conter ao menos uma letra maiúscula, '
            'uma letra minúscula e um número, e deve conter '
            'ao menos 8 caracteres.'
        ),
        validators=[strong_password],
        label='Senha'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Confirmação de senha',
        error_messages={
            'required': 'Por favor, repita sua senha.'
        },
    )

    class Meta:
        model = User
        fields = [
            'user_type',
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'User e-mail is already in use', code='invalid',
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'A senha e a confirmação de senha devem ser iguais.',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                ],
            })
