from clients.status_api import StatusApi

def test_ping(status_api: StatusApi) -> None:
    request = status_api.get_status()
    response = request.json()

    assert request.status_code == 200
    assert response.get('database') == True
