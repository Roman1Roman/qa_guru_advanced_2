from http import HTTPStatus
import pytest
import requests
from clients.users_api import UsersApi
from tests.test_api import fill_test_data


@pytest.mark.usefixtures('fill_test_data')
def test_post_create_user(users_api: UsersApi, new_user):
    user_data = new_user
    request = users_api.create_user(user_data)
    assert request.status_code == HTTPStatus.CREATED
    request_dict = request.json()
    request_id = request_dict.pop('id')
    assert request_dict == new_user
    users_api.delete_user(request_id)


@pytest.mark.usefixtures('fill_test_data')
def test_update_user(users_api: UsersApi, create_new_user, updated_user_name):
    user_id = create_new_user
    request = users_api.update_user(user_id=user_id, data=updated_user_name)
    assert request.status_code == HTTPStatus.OK
    response = request.json()
    response.pop('id')
    assert response == updated_user_name
    users_api.delete_user(user_id)


@pytest.mark.usefixtures('fill_test_data')
def test_delete(users_api: UsersApi, create_new_user):
    user_id = create_new_user
    request = users_api.delete_user(user_id)
    assert request.status_code == HTTPStatus.OK
    checking_request = users_api.get_user(user_id)
    assert checking_request.status_code == HTTPStatus.NOT_FOUND
    checking_request = checking_request.json()
    users_api.delete_user(checking_request.get('id'))


@pytest.mark.usefixtures('fill_test_data')
def test_create_user_invalid_method(users_api: UsersApi, new_user):
    response = users_api.update_user(user_id='', data=new_user)
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
    assert response.json().get('detail') == "Method Not Allowed"


@pytest.mark.usefixtures('fill_test_data')
def test_patch_unprocessable_entity(users_api: UsersApi, updated_user_name):
    user_id = 0
    request = users_api.update_user(user_id, updated_user_name)
    assert request.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.usefixtures('fill_test_data')
def test_patch_not_found(users_api: UsersApi, create_new_user, updated_user_name):
    user_id = create_new_user + 1
    request = users_api.update_user(user_id, updated_user_name)
    assert request.status_code == HTTPStatus.NOT_FOUND
    response = request.json()
    users_api.delete_user(response.get('id'))


@pytest.mark.usefixtures('fill_test_data')
def test_delete_unprocessable_entity(users_api: UsersApi):
    user_id = 0
    request = users_api.delete_user(user_id)
    assert request.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.usefixtures('fill_test_data')
def test_delete_not_found(users_api: UsersApi, create_new_user, updated_user_name):
    user_id = create_new_user + 1
    request = users_api.update_user(user_id, updated_user_name)
    assert request.status_code == HTTPStatus.NOT_FOUND
    users_api.delete_user(create_new_user)


@pytest.mark.usefixtures('fill_test_data')
def test_post_unprocessable_entity(users_api: UsersApi, new_user):
    new_user.pop('first_name')
    user_data = new_user
    request = users_api.create_user(user_data)
    assert request.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
