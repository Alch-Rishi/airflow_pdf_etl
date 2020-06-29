from setting.config import ELASTICSEARCH, TIKA_SERVER
import requests

import json


def publish_to_es(payload):

    try:
        url = ELASTICSEARCH['URL'] + '/' + ELASTICSEARCH['INDEX'] + '/' + ELASTICSEARCH['DOC_TYPE']
        response = requests.post(url, headers=ELASTICSEARCH['HEADERS'], data=json.dumps(payload), timeout=ELASTICSEARCH['TIMEOUT']) 
        print("Response time " + str(response.elapsed.total_seconds()))
        sts_cd = response.status_code
        print("\n\n\n----- Es response--------")
        print(response.content)
        print(response)
        elastic_response = response.json()
        if sts_cd in range(200, 300):
            print("-------------------------------")
            return {'status': True, 'data': elastic_response}
        return {'status': False, 'error': elastic_response}
    except Exception as error:
        return {'status': False, 'error': "Elastic search error {}".format(error)}

def get_tika_content(payload):

    try:
        url = TIKA_SERVER['URL'] + '/tika'
        response = requests.put(url, data=payload, headers=TIKA_SERVER['CONTENT_HEADERS'], timeout=TIKA_SERVER['TIMEOUT']) 
        print("Response time " + str(response.elapsed.total_seconds()))
        sts_cd = response.status_code
        tika_response = response.text
        if sts_cd in range(200, 300):
            print("-------------------------------")
            return {'status': True, 'data': tika_response}
        return {'status': False, 'error': tika_response}
    except Exception as error:
        return {'status': False, 'error': "Tika server error {}".format(error)}

def get_tika_metadeta(payload):

    try:
        url = TIKA_SERVER['URL'] + "/meta"
        response = requests.put(url, data=payload, headers=TIKA_SERVER['META_HEADERS'], timeout=TIKA_SERVER['TIMEOUT']) 
        print("Response time " + str(response.elapsed.total_seconds()))
        sts_cd = response.status_code
        tika_response = json.loads(response.text)
        if sts_cd in range(200, 300):
            print("-------------------------------")
            return {'status': True, 'data': tika_response}
        return {'status': False, 'error': tika_response}
    except Exception as error:
        return {'status': False, 'error': "Tika server error {}".format(error)}