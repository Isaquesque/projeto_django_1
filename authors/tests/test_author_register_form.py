from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.contrib.auth.models import User


class TestAuthorRegisterForm(TestCase):
    def setUp(self):
        data = {
            "first_name":"Pedro",
            "last_name":"Silva",
            "username":"PSilva",
            "email":"PSilva@gmail.com",
            "password":"12345678",
            "password2":"123456789"
        }
        self.data = data

    @parameterized.expand(
        [
            ("first_name","Ex:. Pedro"),
            ("last_name","Ex:. Silva"),
            ("username","Ex:. PSilva"),
            ("email","Ex:. PSilva@gmail.com"),
            ("password","Sua senha aqui"),
            ("password2","Confirme sua senha aqui"),
        ]
    )
    def test_register_form_placeholders(self,field_name, expected_placeholder):
        form = RegisterForm()
        placeholder = form.fields[field_name].widget.attrs["placeholder"]
        self.assertEqual(placeholder, expected_placeholder)

    @parameterized.expand(
        [
            ("first_name","Primeiro nome"),
            ("last_name","Último nome"),
            ("username","Usuário"),
            ("email","Endereço de Email"),
            ("password","Senha"),
            ("password2","Confirmação"),
        ]
    )
    def test_register_form_labels(self, field_name, expected_label):
        form = RegisterForm()
        label = form.fields[field_name].label
        self.assertEqual(label, expected_label)

    @parameterized.expand(
        [
            ("first_name","Coloque aqui seu primeiro nome"),
            ("last_name","Coloque aqui seu sobrenome"),
            ("username","Coloque aqui o nome que quer que outros vejam. Apenas Letras, números e @/./+/-/_"),
            ("password","A senha deve ter no mínimo 8 caracteres, deve conter também letras maiúsculas, minúsculas, números e simbolos."),
            ("password2","Coloque aqui a mesma senha que colocou no campo de senha"),
        ]
    )
    def test_register_form_help_texts(self, field_name, expected_help_text):
        form = RegisterForm()
        help_text = form.fields[field_name].help_text
        self.assertEqual(help_text, expected_help_text)

    @parameterized.expand(
        [
            ("username","O nome de usuário é obrigatório"),
            ("email","O endereço de email é obrigatório"),
            ("password","A senha é obrigatória"),
            ("password2","A senha de confirmação é obrigatória"),
        ]
    )
    def test_regster_form_error_messages_when_field_input_is_empty(self, field_name, expected_errors):
        self.data[field_name] = ""
        form = RegisterForm(self.data)
        field_errors = form.errors.get(field_name)
        self.assertIn(expected_errors,field_errors)

    @parameterized.expand(
        [
            ("first_name","Este campo deve ter no mínimo 2 caracteres"),
            ("last_name","Este campo deve ter no mínimo 2 caracteres"),
            ("username","Este campo deve ter no mínimo 2 caracteres"),
            ("password","A senha deve ter no mínimo 8 caracteres"),
            ("password2","A senha de confirmação deve ter no mínimo 8 caracteres"),
        ]
    )
    def test_register_form_error_messages_when_field_input_value_is_less_then_min_length(self, field_name, expected_errors):
        self.data[field_name] = "a"
        form = RegisterForm(self.data)
        field_errors = form.errors.get(field_name)
        self.assertIn(expected_errors,field_errors)

    @parameterized.expand(
        [
            ("first_name","Este campo deve ter no máximo 150 caracteres"),
            ("last_name","Este campo deve ter no máximo 150 caracteres"),
            ("username","Este campo deve ter no máximo 150 caracteres"),
            ("password","A senha deve ter no máximo 150 caracteres"),
            ("password2","A senha de confirmação deve ter no máximo 150 caracteres"),
        ]
    )
    def test_register_form_error_messages_when_field_input_value_is_great_then_max_length(self, field_name, expected_errors):
        self.data[field_name] = "a" * 151
        form = RegisterForm(self.data)
        field_errors = form.errors.get(field_name)
        self.assertIn(expected_errors,field_errors)

    def test_register_form_error_messages_when_username_is_invalid(self):
        self.data["username"] = "abc#"
        form = RegisterForm(self.data)
        field_errors = form.errors.get("username")
        self.assertIn("Nome de usuário inválido",field_errors)
    
    def test_register_form_error_messages_when_email_is_invalid(self):
        self.data["email"] = "abc#@d"
        form = RegisterForm(self.data)
        field_errors = form.errors.get("email")
        self.assertIn("Email inválido. Tente novamente com um email válido",field_errors)

    def test_register_form_error_messages_when_email_already_exists(self):
        user = User.objects.create_user("user", "user@gmail.com", "12345678")

        self.data["email"] = "user@gmail.com"
        form = RegisterForm(self.data)
        field_errors = form.errors.get("email")
        self.assertIn("Email já cadastrado. Tente novamente com outro email",field_errors)

    def test_register_form_error_messages_when_username_already_exists(self):
        user = User.objects.create_user("user", "user@gmail.com", "12345678")

        self.data["username"] = "user"
        form = RegisterForm(self.data)
        field_errors = form.errors.get("user")
        self.assertIn("Nome de usuário já em uso. Tente novamente com outro nome de usuário",field_errors)

    def test_register_form_error_messages_when_password_is_invalid(self):
        self.data["password"] = "12345678"
        form = RegisterForm(self.data)
        field_errors = form.errors.get("password")
        self.assertIn("Senha fraca. Tente novamente com uma senha válida.",field_errors)