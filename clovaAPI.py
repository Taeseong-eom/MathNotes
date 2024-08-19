import requests
import uuid
import time
import base64
import json



api_url = 'https://wl11rjimfa.apigw.ntruss.com/custom/v1/30859/ea5fcbc02c05c115b55bbe64469072ec865b2fb60e1ee0fe60eb45dfb4d7e2c7/general'
secret_key = 'ZlRDYlNTZk5RRlFxWW9hY1RjQkR3dVRjSlFmVE1pQUY='
image_file = 'capture/equation.png'

def getEquation():
    with open(image_file, 'rb') as f:
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

    response = requests.request("POST", api_url, headers=headers, data=payload)
    
    ocr_result = json.loads(response.text)
    recognized_text = ""
    
    for field in ocr_result["images"][0]["fields"]:
        # print(field.keys())
        x = []; y = []
        bounding_box = field["boundingPoly"]['vertices']
        for box in bounding_box:
            print(box, type(box))
            # box = json.loads(box)
            x.append(box['x']); y.append(box['y'])
        Xmax = max(x); Xmin = min(x)
        Ymax = max(y); Ymin = min(y)

        recognized_text += field["inferText"] + " "
    
    recognized_text = recognized_text.strip()
    print("OCR 인식된 전체 텍스트: " + recognized_text)
    return recognized_text, Xmax, Xmin, Ymax, Ymin
