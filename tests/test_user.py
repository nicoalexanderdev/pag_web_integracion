import pytest
from django.contrib.auth.models import User
from django.urls import reverse


# crear usuario
@pytest.mark.django_db
def test_user_create():
    user = User.objects.create_user(
        username='usuarioTest',
        first_name= 'usuario',
        last_name= 'Test',
        email = 'usuarioTest@correo.com',
        password='dasdasdf'
    )
    assert user.username == 'usuarioTest'


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
