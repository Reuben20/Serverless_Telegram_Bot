import json
import os
import requests

def req(type,category):
    url = 'https://api.waifu.pics/'+type+'/'+category
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return data.get('url') 


def lambda_handler(event, context):
    
    telegram_msg = "No funciono intentalo denuevo"

    data = event['message']['text']

    if data[0] == '/':
        if data[1:] == 'hentai':
            telegram_msg = req('nsfw','waifu')
        elif data[1:] == 'trap':
            telegram_msg = req('nsfw', 'trap')
        elif data[1:] == 'neko':
            telegram_msg = req('nsfw', 'neko')
        elif data[1:] == 'blowjob':
            telegram_msg = req('nsfw','blowjob')
        else:
            try:
                telegram_msg = req('sfw',data[1:])
            except:
                pass
    
    chat_id = os.environ['CHAT_ID']
    telegram_token = os.environ['TELEGRAM_TOKEN']

    api_url = f"https://api.telegram.org/bot{telegram_token}/"

    params = {'chat_id': chat_id, 'text': telegram_msg}
    res = requests.post(f"{api_url}sendMessage", data=params).json()

    if res["ok"]:
        return {
            'statusCode': 200,
            'body': res['result'],
        }
    else:
        return {
            'statusCode': 400,
            'body': res
        }