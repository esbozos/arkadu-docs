# EJEMPLO DE REGISTRO DE MOVIMIENTOS DE CUENTA AL API DE ARKADU
# 2020-03-02

import json
import requests

def report_movements():
    """
        Registra los movimientos y balance actual de cuenta
    """

    url = "https://old.arkadu.com/api/shop/account/report/"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer vUQzaKhCo9LpPfBAeAetUFQvv24ioC"
    }
    body = {
    "account": "0100-0001-08-0006051619",
    "current_balance": "450000000000.05",
    "customer_id": "2",
    "movements": [
        {
            "reference": "ADC4D3DS",
            "amount": "230202.09",
            "operation": "debit",
            "created": "2020-03-30",
            "note": "Comisión de recaudo...."
        },
        {
            "reference": "ADC400005",
            "amount": "93000202.09",
            "operation": "credit",
            "created": "2020-03-30",
            "note": "Pago en linea homebanking"
        },
        {
            "reference": "ADC400005",
            "amount": "140000000000.00",
            "operation": "credit",
            "created": "2020-03-30",
            "note": "Transferencia internacional recibida"
        },
        ...
    ]
}

    result = requests.post(url, data=json.dumps(body), headers=headers)
    return result

report = report_movements()
print(report.json())

