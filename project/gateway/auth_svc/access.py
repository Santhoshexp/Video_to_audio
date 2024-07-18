"""Module """

import os
import requests

def login(request):
    """Method"""
    auth = request.authorization
    print(auth,'check')
    if not auth:
        return None, ("Missing Credentials",401)
    basciauth = (auth.username,auth.password)

    resp = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login",
        auth = basciauth
    )

    if resp.status_code == 200:
        return resp.text ,None
    return None ,(resp.text,resp.status_code)

