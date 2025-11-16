from http import HTTPStatus
import json
import pytest
from pathlib import Path
from app.models.User import User
from app.models.Pagination import Pagination
from clients.users_api import UsersApi


# Получаем путь к корню проекта
BASE_DIR = Path(__file__).parent.parent
USERS_JSON_PATH = BASE_DIR / "tests" / "users.json"

@pytest.fixture(scope="module")
def fill_test_data(users_api: UsersApi):
    with open(USERS_JSON_PATH, 'r') as f:
        test_data_users = json.load(f)
    api_users = []
    for user in test_data_users:
        response = users_api.create_user(user)
        api_users.append(response.json())

    user_ids = [user["id"] for user in api_users]

    yield user_ids

    for user_id in user_ids:
        users_api.delete_user(user_id)


@pytest.fixture()
def get_users(users_api: UsersApi) -> dict:
    response = users_api.get_users()
    assert response.status_code == HTTPStatus.OK
    return response.json().get('items')


@pytest.mark.usefixtures('fill_test_data')
def test_users(users_api: UsersApi) -> None:
    response = users_api.get_users()
    assert response.status_code == HTTPStatus.OK

    users = response.json().get('items')
    for user in users:
        assert User.model_validate(user)


def test_user(users_api: UsersApi, fill_test_data) -> None:
    for user_id in (fill_test_data[0], fill_test_data[-1]):
        response = users_api.get_user(user_id)
        assert response.status_code == HTTPStatus.OK
        user = response.json()
        User.model_validate(user)


@pytest.mark.parametrize('user_id', [13])
def test_nonexistent_user(users_api: UsersApi, user_id) -> None:
    response = users_api.get_user(user_id)
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.parametrize('user_id', [0, -1, 'test'])
def test_invalid_user(users_api: UsersApi, user_id) -> None:
    response = users_api.get_user(user_id)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.usefixtures('fill_test_data')
def test_users_no_duplicates(get_users) -> None:
    users_ids = [user_id.get('id') for user_id in get_users]
    print(users_ids)
    assert len(users_ids) == len(set(users_ids))


def test_pagination_model(users_api: UsersApi) -> None:
    response = users_api.get_users({"page": 1, "size": 1})
    assert response.status_code == HTTPStatus.OK
    assert Pagination.model_validate(response.json())


@pytest.mark.parametrize('page, size, objects_expected', [
    (1, 5, 5),
    (3, 5, 2),
])
def test_users_object_count(users_api: UsersApi, page, size, objects_expected) -> None:
    response = users_api.get_users({"page": page, "size": size})
    assert response.status_code == HTTPStatus.OK
    assert response.json().get('size') == size
    assert response.json().get('page') == page
    assert len(response.json().get('items')) == objects_expected


@pytest.mark.parametrize('size, pages_expected', [
    (1, 12),
    (2, 6),
    (12, 1),
])
def test_user_pages(users_api: UsersApi, size, pages_expected) -> None:
    response = users_api.get_users({"size": size})
    assert response.status_code == HTTPStatus.OK
    assert response.json().get('size') == size
    assert response.json().get('pages') == pages_expected


@pytest.mark.parametrize('page, size_expected', [
    (1, 12),
    (2, 0),
])
def test_user_object_size(users_api: UsersApi, page, size_expected) -> None:
    response = users_api.get_users({"page": page})
    assert response.status_code == HTTPStatus.OK
    assert response.json().get('page') == page
    assert len(response.json().get('items')) == size_expected
