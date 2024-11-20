from config import prodpayments_collection, produsers_collection
from bson import ObjectId
import requests

query = {
    "order_amount": {"$in": [999, "999"]},
    "payment_status": "SUCCESS",
    "invoice_link": None
}
pending_payments = prodpayments_collection.find(query)

xdict = {
    "data": {
        "order": {
            "order_id": "1e074056-2a2c-4dc2-8a3b-e286fee528f6",
            "order_amount": 999.00,
            "order_currency": "INR",
            "order_tags": None
        },
        "payment": {
            "cf_payment_id": 3231887607,
            "payment_status": "SUCCESS",
            "payment_amount": 999.00,
            "payment_currency": "INR",
            "payment_message": "00::TRANSACTION HAS BEEN APPROVED",
            "payment_time": "2024-11-14T17:47:29+05:30",
            "bank_reference": "431905048734",
            "auth_id": None,
            "payment_method": {
                "upi": {
                    "channel": None,
                    "upi_id": "smita.d.pandey@oksbi"
                }
            },
            "payment_group": "upi"
        },
        "customer_details": {
            "customer_name": "Meenam",
            "customer_id": "67364547ea0dd189e61c10c5",
            "customer_email": None,
            "customer_phone": "8239288256"
        },
        "payment_gateway_details": {
            "gateway_name": "CASHFREE",
            "gateway_order_id": "3489207511",
            "gateway_payment_id": "3231887607",
            "gateway_status_code": None,
            "gateway_order_reference_id": "null",
            "gateway_settlement": "CASHFREE"
        },
        "payment_offers": None
    },
    "event_time": "2024-11-14T17:47:44+05:30",
    "type": "PAYMENT_SUCCESS_WEBHOOK"
}

for payment in pending_payments:
    order_id = payment["order_id"]
    user_id = payment["user_id"]

    user_query = {"_id": ObjectId(user_id)}
    user_details = produsers_collection.find_one(user_query)
    print(user_details)
    user_number = user_details["phoneNumber"]
    user_name = user_details["name"]

    xdict["data"]["order"]["order_id"] = order_id
    xdict["data"]["customer_details"]["customer_id"] = user_id
    xdict["data"]["customer_details"]["customer_name"] = user_name
    xdict["data"]["customer_details"]["customer_phone"] = user_number

    url = "http://localhost:8080/actions/cashfree_webhook"
    response = requests.post(url, json=xdict)
    if response.status_code == 200:
        print("Invoice link updated successfully")
    else:
        print("Invoice link not updated", response.json())
