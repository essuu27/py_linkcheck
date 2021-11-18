import requests
import time
import threading


def webcall(my_url):
        # Unqualified URLs should default to secure http requests
    if not my_url.startswith('http'):
        my_url = 'https://' + my_url

    try:
        response = requests.get(my_url, timeout=10, allow_redirects=True)
        resp_code = response.status_code
    except requests.exceptions.RequestException as req_e:
        print(f"### HTTP error: {req_e}")
        resp_code = "500"

    return(resp_code)

