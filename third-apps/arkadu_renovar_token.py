# EJEMPLO DE RENOVACIÓN DEL TOKEN AL API DE ARKADU
# 2020-03-02

import json
import requests

def renew_token():
    """
        Obtiene un nuevo access_token a través del
        refresh_token provisto por su aliado comercial.

    """

    url = "https://arkadu.comapi/user/access/get-token/"
    headers = {
        "Content-Type": "application/json"
    }

    body = {
        "client_id": "BFrpSg7hLshQcCtmRGCKplFObFBXbe2SrN6Ik3yb",
        "client_secret": "qrqbjHdzd69geHxtN3jVE5TbUgigxy3aRWK07UAGSOUrnzbaDiYUaPaR1J3StbEWR7QXls8vtCt6tXwcF4y3E1ziQShDHqRRmaw0H2qP1dGxltGjz8uCqJV7hLMeQQ5Z",
        "grant_type": "refresh_token",
        "refresh_token": "TJPkSQFKcHYIWErZXLqOYf1qdJasCl"
    }

    result = requests.post(url, data=json.dumps(body), headers=headers)
    return result

new_token = renew_token()
print(new_token.json())