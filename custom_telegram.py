import requests
from configparser import ConfigParser


def send_text(message):
    config_parser = ConfigParser()
    config_parser.read('settings.ini')
    bot_token = config_parser.get('telegram_settings', 'bot_token')
    bot_chat_id = config_parser.get('telegram_settings', 'chat_id')
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chat_id + '&parse_mode=Markdown&text=' + message
    response = requests.get(send_text)
    response = response.json()
    return response
