import requests
from requests.exceptions import RequestException


class MyAPIClient(object):
    """A simple client for the public API."""

    def __init__(self, api_url=None):
        """Constructor."""
        if api_url is None:
            from django.conf import settings
            self._api_url = settings.MY_API_PREFIX
        else:
            self._api_url = api_url

    def _send_request(self, url, params=None):
        """Send a request to the API."""
        if params is None:
            params = {}
        try:
            resp = requests.get(url, params=params)
        except RequestException:
            return None

        if resp.status_code != 200:
            return None

        return resp.json()

    def test_list(self):
        url = "{}/mynewapp/".format(self._api_url)
        return self._send_request(url)
