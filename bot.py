import re
import requests

base_url = "https://api.telegram.org/bot<API_TOKEN>"

def read_msg(offset):
    parameters = {
        "offset": offset
    }

    resp = requests.get(base_url + "/getUpdates", params=parameters)
    data = resp.json()

    for result in data["result"]:
        send_msg(result)

    if data["result"]:
        return data["result"][-1]["update_id"] + 1

def auto_answer(message):
    message = message.strip().lower()
    if message == '/start':
        return "Enter the word to check meaning"

    if re.match(r'^\w+$', message):
        response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{message}')
        if response.status_code == 200:
            return response.json()[0]['meanings'][0]['definitions'][0]['definition']
        else:
            return 'Word not found in the dictionary'
    else:
        return "Please enter a valid single word..."

def send_msg(message):
    chat_id = message["message"]["chat"]["id"]
    text = message["message"]["text"]
    message_id = message["message"]["message_id"]
    answer = auto_answer(text)

    parameters = {
        "chat_id": chat_id,
        "text": answer,
        "reply_to_message_id": message_id
    }

    resp = requests.get(base_url + "/sendMessage", params=parameters)
    print(resp.text)

offset = 0

while True:
    offset = read_msg(offset)
