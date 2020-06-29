
from setting.config import PDF_DIR, INGESTED_DIR, ERROR_ON_INGESTION_DIR
from communicators.client import get_tika_content, get_tika_metadeta, publish_to_es


from datetime import datetime
import os, shutil, sys
import glob
import re

def convert_to_json(data, filepath):

    tika_response_content = get_tika_content(data)
    tika_response_meta = get_tika_metadeta(data)

    if not tika_response_content['status']:
        print(tika_response_content)
        raise Exception(tika_response_content['error'])

    if not tika_response_meta['status']:
        print(tika_response_meta)
        raise Exception(tika_response_meta['error'])

    parsed = {'content':tika_response_content['data'], 'meta':tika_response_meta['data']}

    product_dict = {}
    metadata = parsed['meta']
    #dict_list.append(metadata)

    quick_path = filepath.replace(PDF_DIR, '')
    product_dict['Product Type'] = quick_path.split('/')[1]

    if 'Author' in metadata:
        product_dict['Author'] = metadata['Author']
    else: 
        product_dict['Author'] = ''
        
    #product_dict['Created-By'] = metadata['creator']

    if 'Content-Type' in metadata:
        product_dict['Content Type'] = metadata['Content-Type']
    else: 
        product_dict['Content-Type'] = ''
        
#   if 'Last-Save-Date' in metadata:
#       product_dict['Date Published'] = metadata['Last-Save-Date']
#   else: 
#       product_dict['Date Published'] = ''
    
    product_dict['Date Published'] = datetime.now().isoformat()
        
    if 'title' in metadata:
        product_dict['Title'] = metadata['title']
    else: 
        product_dict['Title'] = ''
        
    product_dict['Text'] = str(re.sub(r'\n\n+', '\n\n', parsed['content']).strip())
   
    basename = os.path.basename(filepath)

    if '-ENG-' in basename:
        product_dict['Language'] = 'English'
        product_dict['langcode'] = 'en'
    if '-ARB-' in basename:
        product_dict['Language'] = 'Arabic'
        product_dict['langcode'] = 'ar'
        
    product_dict['Filename'] = os.path.splitext(basename)[0]
    product_dict['Filepath'] = 'TESTdrive/data' + quick_path
    
    print("\n\n\n-------TIKA--------------")
    print(product_dict)
    print("\n\n\n")

    return product_dict

def push_to_es(json_data):

    es_response = publish_to_es(json_data)

    if not es_response['status']:
        raise Exception(es_response['error'])

    print("\n\n\n\n--------ES------------")
    print(es_response)
    print("\n\n\n")

def move_to_ingested_folder(filepath):

    os.system("move "+ str(filepath) +" "+ INGESTED_DIR + "/")

def process():

    files_on_error = []

    print(sys.argv)

    for filepath in glob.iglob(PDF_DIR + '**/**', recursive=True):
        if os.path.isfile(filepath):
            print("\n\n----FILE-----")
            print(filepath)
            print("------")

            try: 
                data = open(filepath, 'rb').read()

                json_data = convert_to_json(data, filepath)

                push_to_es(json_data)

                move_to_ingested_folder(filepath)

            except Exception as e:
                print(e)
                files_on_error.append(filepath)
    
    if len(files_on_error) > 0:
        raise Exception("Error occured for files:- " + ",".join(files_on_error))
