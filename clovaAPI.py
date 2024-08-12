import requests
import uuid
import time
import base64
import json

api_url = 'API_URL'
secret_key = 'SECRET_KEY'
image_file = 'capture/equation.png'

def getEquation():
    with open(image_file,'rb') as f:
        file_data = f.read()

    request_json = {
        'images': [
            {
                'format': 'jpg',
                'name': 'demo',
                'data': base64.b64encode(file_data).decode()
            }
        ],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }

    payload = json.dumps(request_json).encode('UTF-8')
    headers = {
    'X-OCR-SECRET': secret_key,
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", api_url, headers=headers, data = payload)

    # print(response.text)

    return str(json.loads(response.text)["images"][0]['fields'][0]['inferText'])