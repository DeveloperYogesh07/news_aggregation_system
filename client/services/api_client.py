import requests

class APIClient:
    def __init__(self, base_url="http://127.0.0.1:8000/api/v1"):
        self.base_url = base_url
        self.token = None

    def set_token(self, token: str):
        self.token = token


    def _headers(self):  
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"  
        return headers

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
    
    def put(self, path, data):
        url = self.base_url + path
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        response = requests.put(url, json=data, headers=headers)  
        response.raise_for_status()
        return response.json()

    
    def delete(self, path):
        url = self.base_url + path
        response = requests.delete(url, headers=self._headers())
        response.raise_for_status()
        return response.json()
    
    def get_categories(self):
         return self.get("/categories")
    

