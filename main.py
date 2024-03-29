import time
import requests
import urllib
from datetime import datetime
from configparser import ConfigParser
from urllib.parse import urlencode
import custom_telegram

url = ''


def get_available_vaccine_center(pincode):
    global url
    date = datetime.today().strftime('%d-%m-%Y')
    url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin'
    payload = {'pincode': pincode, 'date': date}
    params = urlencode(payload)
    url += '?' + params
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (K HTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    resp = requests.get(url, headers=headers)
    data = resp.json()
    return data


while True:
    config_parser = ConfigParser()
    config_parser.read('settings.ini')
    pincodes = config_parser.get('region_info', 'pincode')
    pincodes = pincodes.split(",")
    for pincode in pincodes:
        response = get_available_vaccine_center(pincode)
        available_flag = 0
        if response['centers']:
            for center in response['centers']:
                if center['sessions']:
                    for session in center['sessions']:
                        if session['available_capacity'] > 0:
                            available_flag = 1
                    if available_flag == 1:
                        msg = "Vaccine available for pincode:" + str(pincode) + ", Center Name:" + str(center['name']) + ", Total Capacity:" + str(session['available_capacity']) + ", Available Dose1:" + str(session['available_capacity_dose1']) + ", Available Dose2:" + str(session['available_capacity_dose2']) + "  check here: " + urllib.parse.quote_plus(url)
                        custom_telegram.send_text(msg)
                    available_flag = 0

    time.sleep(300)
