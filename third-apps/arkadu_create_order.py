# EJEMPLO CREAR ORDEN AL API DE ARKADU
# 2020-03-02

import json
import requests

def create_order():
    """
       crea una nueva orden con 1 o más productos disponibles para el usuario
    """

    url = "https://old.arkadu.com/api/shop/order/create/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer vUQzaKhCo9LpPfBAeAetUFQvv24ioC"
    }
    body = {
        "user_id": "1451502154",
        "products": ["2052142", "20545154", ]
    }

    result = requests.post(url, data=json.dumps(body), headers=headers)
    return result

nueva_orden = create_order()
print(nueva_orden.json())