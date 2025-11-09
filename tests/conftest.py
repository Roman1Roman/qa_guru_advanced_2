import os
from http import HTTPStatus

import requests
import dotenv
import pytest


@pytest.fixture(autouse=True, scope='session')
def get_env():
    dotenv.load_dotenv()


@pytest.fixture(scope='session')
def get_app_url():
    return os.getenv('API_URL')


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





