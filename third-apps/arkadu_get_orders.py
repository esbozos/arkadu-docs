# EJEMPLO DE CONSULTA DE ORDENES AL API DE ARKADU
# 2020-03-02

import json
import requests

def get_order_for_doc(doc_id):
    """
        Obtiene las ordenes pendientes del usuario 
        y/o productos pendientes de pago que pueden 
        ser agregados para crear una nueva orden.
    """

    url = "https://arkadu.com/api/shop/order/get/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer vUQzaKhCo9LpPfBAeAetUFQvv24ioC"
    }
    body = {
        "country": "VE",
        "doc_id": doc_id
    }

    result = requests.post(url, data=json.dumps(body), headers=headers)
    return result

ordenes = get_order_for_doc('J-40157748-2')
print(ordenes.json())