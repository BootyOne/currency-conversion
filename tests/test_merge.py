import pytest
import requests


class TestMerge:
    def test_valid_data(self):
        url = 'http://127.0.0.1:8080/database?merge=0'
        response = requests.post(url)
        assert response.status_code == 200
        body = response.json()
        assert body['success'] == 1
        assert body['data'] == 'Data was handicapped'

    def test_merge(self):
        url = 'http://127.0.0.1:8080/database?merge=1'
        data = {'JPY': 110.0, 'KRW': 1174.5}
        response = requests.post(url, json=data)

        assert response.status_code == 200
        body = response.json()
        assert body['success'] == 1
        assert body['data'] == 'Data stored successfully'

        url = "http://127.0.0.1:8080/convert?from=JPY&to=KRW&amount=1"
        resp = requests.get(url)
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] == 1
        assert data["data"]["from"] == "JPY"
        assert data["data"]["to"] == "KRW"
        assert data["data"]["amount"] == 1
        assert data["data"]["result"] == pytest.approx(10.68, 0.01)

    def test_invalid_json(self):
        url = 'http://127.0.0.1:8080/database?merge=1'
        response = requests.post(url, json='invalid json')

        assert response.status_code == 400
        body = response.json()
        assert body['success'] == 0
        assert body['data'] == 'Invalid JSON data'
