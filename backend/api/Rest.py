import requests

class ApiRest(object):

    def __init__(self, endpoint, filters=''):
        self._baseUrl = 'http://localhost:3001'
        self._endpoint = endpoint
        self._filters = filters
        self._url = f'{self._baseUrl}/{self._endpoint}'

    def get(self):
        try:
            response = requests.get(self._url)
            if response.status_code == 200:
                return response.json()
            else:
                return []
        except Exception:
            return []


if __name__ == "__main__":
    apiRest = ApiRest('extract_companies')
    print(type(apiRest.get()))