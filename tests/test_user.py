import pytest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.messages import get_messages
from django.urls import reverse


# crear usuario
@pytest.mark.django_db
def test_registro_view(client):

    # URL de la vista de registro
    url = reverse('registro')

    # Datos simulados de registro
    data = {
        'username': 'testuser',
        'password1': 'testpassword',
        'password2': 'testpassword',
    }

    # Realizar solicitud POST con los datos simulados
    response = client.post(url, data)

    # Verificar que la solicitud fue exitosa y redirige a 'home'
    assert response.status_code == 302
    assert response.url == reverse('home')

    # Verificar que el usuario está autenticado
    user = authenticate(username='testuser', password='testpassword')
    assert user is not None
    assert user.is_authenticated

    # Verificar mensaje de éxito
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert str(messages[0]) == 'Te has registrado correctamente'

    # Verificar caso de formulario inválido
    invalid_data = {
        'username': '',
        'password1': '',
        'password2': '',
    }
    response_invalid = client.post(url, invalid_data)

    # Verificar que la solicitud no redirige y muestra un mensaje de error
    assert response_invalid.status_code == 200  # Puede ser 200 si no se redirige
    messages_invalid = list(get_messages(response_invalid.wsgi_request))
    assert str(messages_invalid[1]) == 'No se ha podido registrar, intente nuevamente'


# iniciar sesion
@pytest.mark.django_db
def test_user_login(client):

    user = User.objects.create_user(
        username='usuarioTest',
        first_name= 'usuario',
        last_name= 'Test',
        email = 'usuarioTest@correo.com',
        password='dasdasdf'
    )

    login_url = reverse('login')  
    response = client.post(login_url, {
        'username': user.username,
        'password': 'dasdasdf'
    })

    # Verificar que la respuesta fue un redireccionamiento (lo que implica que el login fue exitoso)
    assert response.status_code == 302
    assert response.url == '/'

    assert client.session['_auth_user_id'] == str(user.id)
