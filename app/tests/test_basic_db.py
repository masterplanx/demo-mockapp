# pip install pytest requests
# py.test
import requests


def test_home():
    "GET request to url returns a 200"
    url = 'http://demo-mockapp.jx-staging.flugel.it/'
    resp = requests.get(url)
    assert resp.status_code == 200
