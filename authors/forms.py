from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Primeiro nome",
        widget=forms.TextInput(attrs={
            "placeholder":"Ex:. Pedro"
        }),
        help_text="Coloque aqui seu primeiro nome",
        error_messages={
            "min_length":"Este campo deve ter no mínimo 2 caracteres",
            "max_length":"Este campo deve ter no máximo 150 caracteres"
        },
        required=False,
        max_length= 150,
        min_length = 2
    )
    last_name = forms.CharField(
        label="Último nome",
        widget=forms.TextInput(attrs={
            "placeholder":"Ex:. Silva"
        }),
        help_text="Coloque aqui seu sobrenome",
        error_messages={
            "min_length":"Este campo deve ter no mínimo 2 caracteres",
            "max_length":"Este campo deve ter no máximo 150 caracteres"
        },
        required=False,
        max_length= 150,
        min_length = 2
    )
    username = forms.CharField(
        label="Usuário",
        widget=forms.TextInput(attrs={"placeholder":"Ex:. PSilva"}),
        help_text="Coloque aqui o nome que quer que outros vejam.\n" \
        "Apenas Letras, números e @/./+/-/_",
        error_messages={
            "invalid":"Nome de usuário inválido",
            "required":"O nome de usuário é obrigatório",
            "min_length":"Este campo deve ter no mínimo 2 caracteres",
            "max_length":"Este campo deve ter no máximo 150 caracteres"
        },
        min_length=2,
        max_length=150,
        required=True
    )

    email = forms.CharField(
        label="Endereço de Email",
        widget=forms.EmailInput(attrs={"placeholder":"Ex:. PSilva@gmail.com"}),
        error_messages={
            "invalid":"Endereço de email inválido",
            "required":"O endereço de email é obrigatório"
        },
        required=True
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder":"Sua senha aqui"}
        ),
        label="Senha",
        help_text="A senha deve ter no mínimo 8 caracteres, deve conter também letras maiúsculas, minúsculas, números e simbolos.",
        error_messages={
            "invalid":"Senha inválida",
            "required":"A senha é obrigatória",
            "min_length":"A senha deve ter no mínimo 8 caracteres",
            "max_length":"A senha deve ter no máximo 150 caracteres",
        },
        min_length=8,
        max_length=150,
        required=True,
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder":"Confirme sua senha aqui"}
        ),
        label="Confirmação",
        help_text="Coloque aqui a mesma senha que colocou no campo de senha",
        error_messages={
            "required":"A senha de confirmação é obrigatória",
            "max_length":"A senha de confirmação deve ter no máximo 150 caracteres",
            "min_length":"A senha de confirmação deve ter no mínimo 8 caracteres",
        },
        min_length=8,
        max_length=150,
        required=True,
    )

    class Meta():
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
        ]
    def clean_username(self):
        username = self.cleaned_data["username"]
        user = User.objects.filter(username = username)
        if user:
            raise ValidationError("Nome de usuário já em uso. Tente novamente com outro nome de usuário")
        return username
    
    def clean_email(self):
        regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        email = self.cleaned_data["email"]

        match = re.fullmatch(regex, email)
        if match is None:
            raise ValidationError("Email inválido. Tente novamente com um email válido")
        
        user = User.objects.filter(email=email)
        if user:
            raise ValidationError("Email já cadastrado. Tente novamente com outro email")

        return email

    def clean_password(self):
        regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!])[A-Za-z\d@#$%^&+=!]{8,}$'
        
        cleaned_data = self.cleaned_data
        password = cleaned_data["password"]
        match = re.fullmatch(regex,password)
        
        if match is None:
            raise ValidationError("Senha fraca. Tente novamente com uma senha válida.")
        
        return password


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            self.add_error("password2", "A senha de confirmação deve ser a mesma do campo Senha")
        return cleaned_data