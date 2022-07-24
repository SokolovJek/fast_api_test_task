import json


def test_create_user(client):
    data = {'username': 'testuser',
            'email': 'testuser@mail.com',
            'password': 'test123'}
    response = client.post('/user/register', json.dumps(data))
    assert response.status_code == 200
    assert response.json()['email'] == 'testuser@mail.com'
    assert response.json()['is_active']


def test_login_user(client):
    data = {'username': 'testuser',
            'email': 'testuser@mail.com',
            'password': 'test123'}
    client.post('/user/register', json.dumps(data))

    data = {'username': 'testuser@mail.com',
            'password': 'test123'}

    response = client.post('/login', data=data)

    assert response.status_code == 200
    assert response.json()['token_type'] == 'bearer'


def test_login_user_fake_password(client):
    data = {'username': 'testuser',
            'email': 'testuser@mail.com',
            'password': 'test123'}
    client.post('/user/register', json.dumps(data))

    data = {'username': 'testuser@mail.com',
            'password': 'test122'}
    response = client.post('/login', data=data)
    assert response.status_code == 401
    assert response.json()['detail'] == "Некоректный логин или пароль"


def test_read_user(client, normal_user_token_headers):
    msg = client.post("/user/1", headers=normal_user_token_headers)
    assert msg.status_code == 200
    assert msg.json()['email'] == 'test@example.com'
    assert msg.json()['is_active']


def test_read_user_fake_data(client, normal_user_token_headers):
    data = {'username': 'testuser',
            'email': 'testuser@mail.com',
            'password': 'test123'}
    client.post('/user/register', json.dumps(data))

    msg = client.post("/user/3", headers=normal_user_token_headers)
    assert msg.status_code == 404
    assert msg.json()['detail'] == 'Пользователя с идентификатором 3 не существует'


def test_read_user_not_have_permission(client, normal_user_token_headers):
    data = {'username': 'testuser',
            'email': 'testuser@mail.com',
            'password': 'test123'}
    client.post('/user/register', json.dumps(data))

    msg = client.post("/user/2", headers=normal_user_token_headers)
    assert msg.status_code == 401
    assert msg.json()['detail'] == f"Вам не разрешено просмптривать пользователя с id № 2," \
                                   f" так как вы не владелец учетной записи № 2!!!!"


def test_get_refresh_token_fake(client):
    data = {'username': 'testuser',
            'email': 'testuser@mail.com',
            'password': 'test123'}
    client.post('/user/register', json.dumps(data))

    data = {'username': 'testuser@mail.com',
            'password': 'test123'}

    response = client.post('/login', data=data)

    assert response.status_code == 200
    assert response.json()['token_type'] == 'bearer'
    refresh_token = response.json()['refresh_token']
    print('dddd=-------', refresh_token)
    response = client.post('/refresh_jwt', data=refresh_token)
    assert response.status_code == 401
    assert response.json()['detail'] == "Недействительный токен"


def test_get_refresh_token(client):
    data = {'username': 'testuser',
            'email': 'testuser@mail.com',
            'password': 'test123'}
    client.post('/user/register', json.dumps(data))

    data = {'username': 'testuser@mail.com',
            'password': 'test123'}

    response = client.post('/login', data=data)
    refresh_token = response.json()['refresh_token']
    data = {'refresh_token': refresh_token}
    response = client.post('/refresh_jwt', json=data)
    assert response.status_code == 200
    assert response.json()['access_token']
    assert response.json()['refresh_token']
