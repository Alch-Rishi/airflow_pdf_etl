
from setting.config import PDF_DIR, INGESTED_DIR, ERROR_ON_INGESTION_DIR
from communicators.client_service import parse_through_tika, publish_to_es

import os, shutil
import glob

def convert_to_json(data):

    tika_response = parse_through_tika(data)

    if not tika_response['status']:
        raise Exception(tika_response['error'])

    print(tika_response['data'])
    return tika_response['data']

def push_to_es(json_data):

    es_response = publish_to_es(json_data)

    if not es_response['status']:
        raise Exception(es_response['error'])

    print(es_response)

def move_to_ingested_folder(filepath):

    shutil.move(filepath, INGESTED_DIR)

def process():

    try:
        for filepath in glob.iglob(PDF_DIR + '**/**', recursive=True):
            if os.path.isfile(filepath):
                data = open(filepath, 'rb').read()

                json_data = convert_to_json(data)

                push_to_es(json_data)

                move_to_ingested_folder(filepath)

    except Exception as e:
        print(e)
        raise Exception(e)
