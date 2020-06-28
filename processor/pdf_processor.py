
from setting.config import PDF_DIR, INGESTED_DIR, ERROR_ON_INGESTION_DIR
from communicators.client_service import parse_through_tika, publish_to_es

import os, shutil
import glob

def convert_to_json(data):

    tika_response = parse_through_tika(data)

    if not tika_response['status']:
        raise Exception(tika_response['error'])
    print("\n\n\n-------TIKA--------------")
    print(tika_response['data'])
    print("\n\n\n")
    return tika_response['data']

def push_to_es(json_data):

    es_response = publish_to_es(json_data)

    if not es_response['status']:
        raise Exception(es_response['error'])

    print("\n\n\n\n--------ES------------")
    print(es_response)
    print("\n\n\n")

def move_to_ingested_folder(filepath):

    shutil.move(filepath, INGESTED_DIR)

def process():

    try:
        print(PDF_DIR)
        fileName = PDF_DIR + "/Archive Final Package/Archive 2018 - By Week/English/TEST-18-0038-ENG-arab-iranian-and-turkish-responses-to-president-trumps-impeachment-en-06022018.pdf"
        # print(open(fileName, 'rb').read())
        for filepath in glob.iglob(PDF_DIR + '**/**', recursive=True):
            if os.path.isfile(filepath):
                print("\n\n----FILE-----")
                print(filepath)
                print("--------------")
                data = open(filepath, 'rb').read()

                json_data = convert_to_json(data)

                push_to_es(json_data)

                move_to_ingested_folder(filepath)

    except Exception as e:
        print(e)
        raise Exception(e)
