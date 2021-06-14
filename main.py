import iyzipay
from flask import Flask, render_template, url_for, session, redirect, flash, jsonify, request
import json

app = Flask(__name__)

options = {
    'api_key': 'sandbox-mZgRGbYvHD89G5lro8yogH7ls7V1h3oB',
    'secret_key': 'sandbox-zlpHQkWcxApsLhmRbE6cXq99wRJ5rqE4',
    'base_url': 'sandbox-api.iyzipay.com'
}


@app.route('/')
def index():
    buyer = {
        'id': 'BY789',
        'name': 'John',
        'surname': 'Doe',
        'gsmNumber': '+905350000000',
        'email': 'email@email.com',
        'identityNumber': '74300864791',
        'lastLoginDate': '2015-10-05 12:43:35',
        'registrationDate': '2013-04-21 15:12:09',
        'registrationAddress': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
        'ip': '85.34.78.112',
        'city': 'Istanbul',
        'country': 'Turkey',
        'zipCode': '34732'
    }
    address = {
        'contactName': 'Jane Doe',
        'city': 'Istanbul',
        'country': 'Turkey',
        'address': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
        'zipCode': '34732'
    }
    basket_items = [
        {
            'id': 'BI101',
            'name': 'Binocular',
            'category1': 'Collectibles',
            'category2': 'Accessories',
            'itemType': 'PHYSICAL',
            'price': '0.3'
        },
        {
            'id': 'BI102',
            'name': 'Game code',
            'category1': 'Game',
            'category2': 'Online Game Items',
            'itemType': 'VIRTUAL',
            'price': '0.5'
        },
        {
            'id': 'BI103',
            'name': 'Usb',
            'category1': 'Electronics',
            'category2': 'Usb / Cable',
            'itemType': 'PHYSICAL',
            'price': '0.2'
        }
    ]
    req = {
        'locale': 'tr',
        'conversationId': '123456789',
        'price': '1',
        'paidPrice': '1.2',
        'currency': 'TRY',
        'basketId': 'B67832',
        'paymentGroup': 'PRODUCT',
        "callbackUrl": "https://www.merchant.com/callback",
        "enabledInstallments": ['2', '3', '6', '9'],
        'buyer': buyer,
        'shippingAddress': address,
        'billingAddress': address,
        'basketItems': basket_items
        # 'debitCardAllowed': True
    }

    checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(req, options)
    decoded_str = checkout_form_initialize.read().decode('utf-8')
    json_obj = json.loads(decoded_str)

    payment_page_url = json_obj['paymentPageUrl']
    token = json_obj['token']
    # result(token)

    return redirect(payment_page_url)


@app.route('/result')
def result(token):
    req = {
        'locale': 'tr',
        'conversationId': '123456789',
        'token': token
    }

    checkout_form_result = iyzipay.CheckoutForm().retrieve(req, options)

    print(checkout_form_result.read().decode('utf-8'))
    return None


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
