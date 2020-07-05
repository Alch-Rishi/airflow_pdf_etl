from setting.config import ELASTICSEARCH, TIKA_SERVER, SMTP_SERVER
import requests
import smtplib


import json,sys


def get_past_records(query_string):

    print(query_string)

    try:
        url = ELASTICSEARCH['URL'] + '/' + ELASTICSEARCH['INDEX'] + '/_search'
        response = requests.get(url, headers=ELASTICSEARCH['HEADERS'], data=json.dumps(query_string))
        print("Response time " + str(response.elapsed.total_seconds()))
        sts_cd = response.status_code
        print("\n\n\n----- Es response for get past records--------")
        print(response.content)
        print(response)
        elastic_response = response.json()
        if sts_cd in range(200, 300):
            print("-------------------------------")
            return {'status': True, 'data': elastic_response}
        return {'status': False, 'error': elastic_response}
    except Exception as error:
        return {'status': False, 'error': "Elastic search error {}".format(error)}


def publish_to_es(payload):

    try:
        url = ELASTICSEARCH['URL'] + '/' + ELASTICSEARCH['INDEX'] + '/' + ELASTICSEARCH['DOC_TYPE']
        response = requests.post(url, headers=ELASTICSEARCH['HEADERS'], data=json.dumps(payload), timeout=ELASTICSEARCH['TIMEOUT']) 
        print("Response time " + str(response.elapsed.total_seconds()))
        sts_cd = response.status_code
        print("\n\n\n----- Es response for document push--------")
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
        response = requests.put(url, data=payload,timeout=TIKA_SERVER['TIMEOUT']) 
        print("Response time " + str(response.elapsed.total_seconds()))
        sts_cd = response.status_code
        tika_response = response.content.decode('utf8')
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

def send_email(mail_body):

    try:
        smtpObj = smtplib.SMTP(SMTP_SERVER['HOST'], SMTP_SERVER['PORT'])
        smtpObj.connect(SMTP_SERVER['HOST'], SMTP_SERVER['PORT'])
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.ehlo()
        smtpObj.login(SMTP_SERVER['USERNAME'], SMTP_SERVER['PASSWORD'])
        smtpObj.sendmail(SMTP_SERVER['FROM'], SMTP_SERVER['TO'], mail_body)   
        smtpObj.close()      
        print ("Successfully sent email")
    except Exception as e:
        print ("Error: unable to send email " + str(e))