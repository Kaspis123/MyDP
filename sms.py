
import requests


def main(number,data):

    resp = requests.post('https://textbelt.com/text', {
        'phone': f'{number}',
        'message': f'{data}',
        'key': 'textbelt',
    })

    return resp.json()


