import pytest
import requests


class TestConvertHandler:
    def test_convert_handler(self):
        url = "http://127.0.0.1:8080/convert?from=USD&to=RUR&amount=1"
        resp = requests.get(url)
        assert resp.status_code == 200
        data = resp.json()
        assert data["success"] == 1
        assert data["data"]["from"] == "USD"
        assert data["data"]["to"] == "RUR"
        assert data["data"]["amount"] == 1
        assert data["data"]["result"] == pytest.approx(83.4285, 0.01)

    def test_convert_handler_invalid_currency(self):
        url = "http://127.0.0.1:8080/convert?from=USD&to=XXX&amount=100"
        resp = requests.get(url)
        assert resp.status_code == 400
        data = resp.json()
        assert data["success"] == 0
        assert data["error"] == "Invalid currency"

    def test_convert_handler_invalid_amount(self):
        url = "http://127.0.0.1:8080/convert?from=USD&to=EUR&amount=invalid_value"
        resp = requests.get(url)
        assert resp.status_code == 400
        data = resp.json()
        assert data["success"] == 0
        assert data["error"] == "Invalid amount, should be a number"

    def test_convert_handler_no_params(self):
        url = "http://127.0.0.1:8080/convert"
        resp = requests.get(url)
        assert resp.status_code == 400
        data = resp.json()
        assert data["success"] == 0
        assert data["error"] == "You did not specify currencies"
