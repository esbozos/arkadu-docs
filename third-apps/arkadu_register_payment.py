# EJEMPLO DE REGISTRO DE PAGO DE ORDENES AL API DE ARKADU
# 2020-03-02

import json
import requests

def register_payment():
    """
        Registra el pago de una orden.
    """

    url = "https://old.arkadu.com/api/shop/order/pay/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer vUQzaKhCo9LpPfBAeAetUFQvv24ioC"
    }
    body = {
        "amount": "240000.00",
        "order": "2051963",
        "account": "0100-0001-08-0006051619",
        "reference": "ABDC0000123",
        "created": "2020-01-30 05:46",
        "user_id": "109679"
    }

    result = requests.post(url, data=json.dumps(body), headers=headers)
    return result

pago = register_payment()
print(pago.json())