import requests

class APIClient:
    def __init__(self, base_url="http://127.0.0.1:8000/api/v1"):
        self.base_url = base_url
        self.token = None

    def set_token(self, token: str):
        self.token = token

    def post(self, endpoint, data=None):
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        response = requests.post(f"{self.base_url}{endpoint}", json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    def get(self, endpoint, params=None):
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        response = requests.get(f"{self.base_url}{endpoint}", params=params, headers=headers)
        response.raise_for_status()
        return response.json()
