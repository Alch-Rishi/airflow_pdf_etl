from communicators.client import get_past_records, send_email
from setting.config import SMTP_SERVER, ELASTICSEARCH

import smtplib


def prepare_and_send_email(count):

    body = "The total ingested document count for past {0} days is {1}".format(str(ELASTICSEARCH['PREV_DAYS']), count)

    message = 'Subject: {}\n\n{}'.format(SMTP_SERVER['SUBJECT'], body)

    send_email(message)

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