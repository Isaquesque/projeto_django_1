from django.test import TestCase, Client
from django.urls import resolve,reverse
from authors.forms import RegisterForm
from django.contrib.auth.models import User
from parameterized import parameterized

class TestAuthorRegisterView(TestCase):
    def setUp(self):
        self.c = Client()
        self.path_register_view = reverse("register")
        self.data = {
            "first_name":"Teste",
            "last_name":"Silva",
            "username":"TSilva",
            "email":"tsilva@gmail.com",
            "password":"abc123A@",
            "password2":"abc123A@"
        }

    def test_author_register_view_get_request(self):
        
        response = self.c.get(self.path_register_view)
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], RegisterForm)
        self.assertEqual(response.context["form"].is_bound, False)
    
    def test_author_register_view_successful_post_request(self):
        response = self.c.post(self.path_register_view, self.data)
        user = User.objects.filter(username=self.data["username"])

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], RegisterForm)
        self.assertEqual(response.context["form"].is_bound, False)

        self.assertIn(f"Usuário {self.data["username"]} cadastrado com sucesso", response.content.decode("utf-8"))
        self.assertIsNotNone(user)

    @parameterized.expand(
            [
                ("first_name", 150,"Este campo deve ter no máximo 150 caracteres"),
                ("last_name", 150,"Este campo deve ter no máximo 150 caracteres"),
                ("username", 150,"Este campo deve ter no máximo 150 caracteres"),
                ("password", 150,"A senha deve ter no máximo 150 caracteres"),
                ("password2", 150,"A senha de confirmação deve ter no máximo 150 caracteres"),
            ]
    )
    def test_author_register_view_error_messages_for_max_length_error(
        self, 
        field_name,  
        expected_max_length,
        error_msg,
    ):
        self.data[field_name] = "a" * (expected_max_length+1)
        response = self.c.post(self.path_register_view, self.data)

        bound_form = response.context["form"]

        self.assertIsInstance(response.context["form"], RegisterForm)
        self.assertEqual(response.context["form"].is_bound, True)

        self.assertIn(error_msg, bound_form[field_name].errors)
        self.assertIn(f"O formulário possui erros. Corrija-os", response.content.decode("utf-8"))

    @parameterized.expand(
            [
                ("first_name", 2, "Este campo deve ter no mínimo 2 caracteres"),
                ("last_name", 2, "Este campo deve ter no mínimo 2 caracteres"),
                ("username", 2, "Este campo deve ter no mínimo 2 caracteres"),
                ("password", 8, "A senha deve ter no mínimo 8 caracteres"),
                ("password2", 8, "A senha de confirmação deve ter no mínimo 8 caracteres"),
            ]
    )
    def test_author_register_view_error_messages_for_min_length_error(
        self, 
        field_name,  
        expected_min_length,
        error_msg,
    ):
        self.data[field_name] = "a" * (expected_min_length-1)
        response = self.c.post(self.path_register_view, self.data)

        bound_form = response.context["form"]

        self.assertIsInstance(response.context["form"], RegisterForm)
        self.assertEqual(response.context["form"].is_bound, True)

        self.assertIn(error_msg, bound_form[field_name].errors)
        self.assertIn(f"O formulário possui erros. Corrija-os", response.content.decode("utf-8"))


    @parameterized.expand(
            [
                ("username", "O nome de usuário é obrigatório"),
                ("email", "O endereço de email é obrigatório"),
                ("password", "A senha é obrigatória"),
                ("password2", "A senha de confirmação é obrigatória"),
            ]
    )
    def test_author_register_view_error_messages_for_empty_field_error(
        self, 
        field_name,
        error_msg
    ):
        self.data[field_name] = ""
        response = self.c.post(self.path_register_view, self.data)

        bound_form = response.context["form"]

        self.assertIsInstance(response.context["form"], RegisterForm)
        self.assertEqual(response.context["form"].is_bound, True)

        self.assertIn(error_msg, bound_form[field_name].errors)
        self.assertIn(f"O formulário possui erros. Corrija-os", response.content.decode("utf-8"))

    def test_author_register_view_error_message_for_invalid_username(self):
        self.data["username"] = "abc#$de"
        response = self.c.post(self.path_register_view, self.data)

        bound_form = response.context["form"]

        self.assertIsInstance(response.context["form"], RegisterForm)
        self.assertEqual(response.context["form"].is_bound, True)

        self.assertIn("Nome de usuário inválido", bound_form["username"].errors)
        self.assertIn(f"O formulário possui erros. Corrija-os", response.content.decode("utf-8"))

    def test_author_register_view_error_message_for_invalid_email(self):
        self.data["email"] = "abcde@efg"
        response = self.c.post(self.path_register_view, self.data)

        bound_form = response.context["form"]

        self.assertIsInstance(response.context["form"], RegisterForm)
        self.assertEqual(response.context["form"].is_bound, True)

        self.assertIn("Email inválido. Tente novamente com um email válido", bound_form["email"].errors)
        self.assertIn(f"O formulário possui erros. Corrija-os", response.content.decode("utf-8"))
    
    def test_author_register_view_error_message_for_invalid_password(self):
        self.data["password"] = "abcdefgh"
        response = self.c.post(self.path_register_view, self.data)

        bound_form = response.context["form"]

        self.assertIsInstance(response.context["form"], RegisterForm)
        self.assertEqual(response.context["form"].is_bound, True)

        self.assertIn("Senha fraca. Tente novamente com uma senha válida.", bound_form["password"].errors)
        self.assertIn(f"O formulário possui erros. Corrija-os", response.content.decode("utf-8"))
    
    def test_author_register_view_error_message_for_invalid_confirmation_password(self):
        self.data["password2"] = "abcdefgh"
        response = self.c.post(self.path_register_view, self.data)

        bound_form = response.context["form"]

        self.assertIsInstance(response.context["form"], RegisterForm)
        self.assertEqual(response.context["form"].is_bound, True)

        self.assertIn("A senha de confirmação deve ser a mesma do campo Senha", bound_form["password2"].errors)
        self.assertIn(f"O formulário possui erros. Corrija-os", response.content.decode("utf-8"))
    
    def test_author_register_view_error_message_for_existing_username(self):

        self.c.post(self.path_register_view, self.data)
        response = self.c.post(self.path_register_view, self.data)

        bound_form = response.context["form"]

        self.assertIsInstance(response.context["form"], RegisterForm)
        self.assertEqual(response.context["form"].is_bound, True)

        self.assertIn("Nome de usuário já em uso. Tente novamente com outro nome de usuário", bound_form["username"].errors)
        self.assertIn(f"O formulário possui erros. Corrija-os", response.content.decode("utf-8"))
    
    def test_author_register_view_error_message_for_existing_email(self):
        self.c.post(self.path_register_view, self.data)
        response = self.c.post(self.path_register_view, self.data)

        bound_form = response.context["form"]

        self.assertIsInstance(response.context["form"], RegisterForm)
        self.assertEqual(response.context["form"].is_bound, True)

        self.assertIn("Email já cadastrado. Tente novamente com outro email", bound_form["email"].errors)
        self.assertIn(f"O formulário possui erros. Corrija-os", response.content.decode("utf-8"))