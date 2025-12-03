import requests
import json
import base64
from datetime import datetime
from django.conf import settings


def get_access_token():
    """
    Authenticates with Daraja API to get an access token.
    """
    try:
        response = requests.get(
            settings.MPESA_AUTH_URL,
            auth=(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET)
        )
        response.raise_for_status()  # Raise error for bad status codes
        result = response.json()
        return result['access_token']
    except Exception as e:
        print(f"Error generating Access Token: {str(e)}")
        return None


def trigger_stk_push(phone_number, amount):
    """
    Initiates the STK Push to the user's phone.
    """
    access_token = get_access_token()
    if not access_token:
        return False, "Failed to authenticate with M-Pesa", None

    # 1. Format Phone Number (Must be 2547XXXXXXXX)
    if phone_number.startswith('0'):
        phone_number = '254' + phone_number[1:]
    elif phone_number.startswith('+254'):
        phone_number = phone_number[1:]

    # 2. Generate Timestamp and Password
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password_str = f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}"
    password = base64.b64encode(password_str.encode()).decode('utf-8')

    # 3. Payload
    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),  # Amount must be an integer
        "PartyA": phone_number,  # The phone sending money
        "PartyB": settings.MPESA_SHORTCODE,  # The organization receiving
        "PhoneNumber": phone_number,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": "IDReplacement",
        "TransactionDesc": "Payment for ID Replacement"
    }

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(settings.MPESA_STK_PUSH_URL, json=payload, headers=headers)
        result = response.json()

        print("\n--- M-PESA API RESPONSE ---")
        print(result)
        print("---------------------------\n")

        # Check if Safaricom accepted the request
        if result.get('ResponseCode') == '0':
            checkout_id = result.get('CheckoutRequestID')
            return True, "STK Push Sent. Check your phone.", checkout_id
        else:
            return False, result.get('errorMessage', 'STK Push Failed'), None

    except Exception as e:
        return False, f"Connection Error: {str(e)}", None


def generate_simulated_transaction_code():
    """Helper to generate a placeholder code since we can't get the real one on localhost easily."""
    import random
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "R" + "".join(random.choice(chars) for _ in range(9))