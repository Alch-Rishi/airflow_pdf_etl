from communicators.client import get_past_records, send_email

import smtplib

def prepare_and_send_email(count):

    mail_body = """From: From Person <from@fromdomain.com>
    To: To Person <to@todomain.com>
    Subject: SMTP e-mail test

    This is a test e-mail message.
    """

    send_email(mail_body)

def get_ingestion_count():

    query_string = '{{"query": {{ "range" : {{ "age" : {{"gte" : now-{0}d,"lte" : now}} }} }} }}'
    response = get_past_records(query_string)

    count = 0

    if response['data']:
        print(response)
    
    return count

def execute():

    try:
        count = get_ingestion_count()
        prepare_and_send_email(count)
    except Exception as e:
        print(e)