from http import HTTPStatus

import requests


def test_post_create_user(get_app_url, new_user):
    user_data = new_user
    request = requests.post(url=f'{get_app_url}/users', json=user_data)
    assert request.status_code == HTTPStatus.CREATED
    response = request.json()
    response.pop('id')
    assert response == new_user
    requests.delete(url=f'{get_app_url}/users/{response.get('id')}')


def test_update_user(get_app_url, create_new_user, updated_user_name):
    user_id = create_new_user
    request = requests.patch(url=f'{get_app_url}/users/{user_id}', json=updated_user_name)
    assert request.status_code == HTTPStatus.OK
    response = request.json()
    response.pop('id')
    assert response == updated_user_name


def test_delete(get_app_url, create_new_user):
    user_id = create_new_user
    request = requests.delete(url=f'{get_app_url}/users/{user_id}')
    assert request.status_code == HTTPStatus.OK
    checking_request = requests.get(url=f'{get_app_url}/users/{user_id}')
    assert checking_request.status_code == HTTPStatus.NOT_FOUND


def test_create_user_invalid_method(get_app_url, new_user):
    response = requests.patch(f"{get_app_url}/users/", json=new_user)
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
    assert response.json().get('detail') == "Method Not Allowed"


def test_patch_unprocessable_entity(get_app_url, updated_user_name):
    user_id = 0
    request = requests.patch(url=f'{get_app_url}/users/{user_id}', json=updated_user_name)
    assert request.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_patch_not_found(get_app_url, create_new_user, updated_user_name):
    user_id = create_new_user + 1
    request = requests.patch(url=f'{get_app_url}/users/{user_id}', json=updated_user_name)
    assert request.status_code == HTTPStatus.NOT_FOUND


def test_delete_unprocessable_entity(get_app_url, create_new_user):
    user_id = 0
    request = requests.delete(url=f'{get_app_url}/users/{user_id}')
    assert request.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_delete_not_found(get_app_url, create_new_user, updated_user_name):
    user_id = create_new_user + 1
    request = requests.patch(url=f'{get_app_url}/users/{user_id}', json=updated_user_name)
    assert request.status_code == HTTPStatus.NOT_FOUND


def test_post_unprocessable_entity(get_app_url, new_user):
    new_user.pop('first_name')
    user_data = new_user
    request = requests.post(url=f'{get_app_url}/users', json=user_data)
    assert request.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
