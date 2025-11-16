from requests import Response

from clients.base_session import BaseSession
from config import Server


class UsersApi:

    def __init__(self, env):
        self.session = BaseSession(base_url=Server(env).app)

    def get_user(self, user_id: int) -> Response:
        return self.session.get(f'/api/users/{user_id}')

    def get_users(self, params=None) -> Response:
        return self.session.get(f'/api/users/', params=params)

    def create_user(self, data: dict) -> Response:
        return self.session.post(f'/api/users/', json=data)

    def update_user(self, user_id: int, data: dict) -> Response:
        return self.session.patch(f'/api/users/{user_id}', json=data)

    def delete_user(self, user_id: int) -> Response:
        return self.session.delete(f'/api/users/{user_id}')
