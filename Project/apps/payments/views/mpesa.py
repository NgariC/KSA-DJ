import base64
from datetime import datetime

import requests
from requests.auth import HTTPBasicAuth

from apps.payments import keys


def get_timestamp():
    return datetime.now().strftime("%Y%m%d%H%M%S")


def generate_access_token():
    consumer_key = keys.consumer_key
    consumer_secret = keys.consumer_secret
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    try:
        r = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    except:
        r = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret), verify=False)
    json_response = (r.json())

    return json_response["access_token"]


def generate_password(formatted_time):
    data_to_encode = keys.business_shortCode + keys.lipa_na_mpesa_passkey + formatted_time

    encoded_string = base64.b64encode(data_to_encode.encode())
    return encoded_string.decode("utf-8")


def lipa_na_mpesa():
    formatted_time = get_timestamp()
    decoded_password = generate_password(formatted_time)
    access_token = generate_access_token()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {access_token}"}
    request = {"BusinessShortCode": keys.business_shortCode, "Password": decoded_password, "Timestamp": formatted_time,
               "TransactionType": "CustomerPayBillOnline", "Amount": 1, "PartyA": keys.phone_number,
               "PartyB": keys.business_shortCode, "PhoneNumber": keys.phone_number,
               "CallBackURL": "https://kenyascouts.co.ke/api/payments/lnm/", "AccountReference": "test aware",
               "TransactionDesc": 'KSA-Portal Payments'}

    response = requests.post(api_url, json=request, headers=headers)
    print(response.text)


# lipa_na_mpesa()


def register_url():
    my_access_token = generate_access_token()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": f"Bearer {my_access_token}"}
    request = {"ShortCode": keys.shortcode, "ResponseType": "Completed",
               "ConfirmationURL": "https://kenyascouts.co.ke/api/payments/c2b-confirmation/",
               "ValidationURL": "https://kenyascouts.co.ke/api/payments/c2b-validation/"}

    try:
        response = requests.post(api_url, json=request, headers=headers)
    except Exception:
        response = requests.post(api_url, json=request, headers=headers, verify=False)
    print(response.text)


# register_url()


def simulate_c2b_transaction():
    my_access_token = generate_access_token()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
    headers = {"Authorization": f"Bearer {my_access_token}"}
    request = {"ShortCode": keys.shortcode, "CommandID": "CustomerPayBillOnline", "Amount": "2896", "Msisdn":
        keys.test_msisdn, "BillRefNumber": "myaccnumber"}

    try:
        response = requests.post(api_url, json=request, headers=headers)
    except Exception:
        response = requests.post(api_url, json=request, headers=headers, verify=False)
    print(response.text)

# simulate_c2b_transaction()
