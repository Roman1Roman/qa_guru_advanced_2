from requests import Response
from clients.base_session import BaseSession
from config import Server

class StatusApi:

    def __init__(self, env):
        self.session = BaseSession(base_url=Server(env).app)

    def get_status(self) -> Response:
        return self.session.get('/api/status', timeout=10)
