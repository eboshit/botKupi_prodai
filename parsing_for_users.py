# -*- coding: utf-8 -*-
import requests

def Btc():
    url_btc = 'https://ru.investing.com/crypto/bitcoin/btc-rub'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86 YaBrowser/21.3.1.185 Yowser/2.5 Safari/537.36'
    }
    response = requests.request("POST", url_btc, headers=HEADERS).text
    response = response.split('<span class="text-2xl" data-test="instrument-price-last">')
    response = response[1].split('</span>')
    response = response[0]
    price_btc = ''
    response = response.split('.')
    for i in response:
        price_btc += i
    price_btc = int(price_btc)
    return price_btc

def Usdt():
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86 YaBrowser/21.3.1.185 Yowser/2.5 Safari/537.36'
    }
    url_usdt = 'https://ru.investing.com/crypto/tether/usdt-rub'

    response = requests.request("POST", url_usdt, headers=HEADERS).text
    response = response.split('<span class="text-2xl" data-test="instrument-price-last">')
    response = response[1].split('</span>')
    response = response[0].replace(',', '.')
    price_usdt = float(response)
    return price_usdt

def Ltc():
    url_ltc = 'https://ru.investing.com/crypto/litecoin/ltc-rub'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86 YaBrowser/21.3.1.185 Yowser/2.5 Safari/537.36'
    }
    response = requests.request("POST", url_ltc, headers=HEADERS).text
    response = response.split('<span class="text-2xl" data-test="instrument-price-last">')
    response = response[1].split('</span>')
    response = response[0].split(',')
    price_ltc = ''
    for i in response[0]:
        for x in i.split('.'):
            price_ltc += x
    price_ltc += '.'+response[1]
    price_ltc = float(price_ltc)
    return price_ltc

def check(url):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.86 YaBrowser/21.3.1.185 Yowser/2.5 Safari/537.36'
    }
    if requests.request("POST", url, headers=HEADERS):
        return True
    else:
        return False

check('https://msk.kupiprodai.ru/1232')

