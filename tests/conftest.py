import os
from http import HTTPStatus
import requests
import dotenv
import pytest
from clients.users_api import UsersApi
from clients.status_api import StatusApi


@pytest.fixture(autouse=True, scope='session')
def get_env():
    dotenv.load_dotenv()


def pytest_addoption(parser):
    parser.addoption('--env', default='dev')


@pytest.fixture(scope='session')
def env(request):
    return request.config.getoption('--env')


@pytest.fixture(scope='session')
def users_api(env):
    api = UsersApi(env)
    yield api
    api.session.close()


@pytest.fixture(scope='session')
def status_api(env):
    api = StatusApi(env)
    yield api
    api.session.close()


@pytest.fixture(scope='session')
def get_app_url():
    return os.getenv('API_URL', 'http://localhost:8081/api')


@pytest.fixture()
def new_user():
    new_user = {
        'first_name': 'test_name',
        'last_name': 'test_surname',
        'email': 'test_email@test.com',
        'avatar': 'http://test.com',
    }
    return new_user


@pytest.fixture()
def updated_user_name(new_user):
    new_user['first_name'] = 'new_name'
    return new_user


@pytest.fixture()
def create_new_user(get_app_url, new_user):
    user_data = new_user
    request = requests.post(url=f'{get_app_url}/users', json=user_data)
    assert request.status_code == HTTPStatus.CREATED
    user_id = request.json().get('id')

    yield user_id

    requests.delete(url=f'{get_app_url}/users/{user_id}')





