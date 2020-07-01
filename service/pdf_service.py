
from setting.config import PDF_DIR, INGESTED_DIR, ERROR_ON_INGESTION_DIR
from communicators.client import get_tika_content, get_tika_metadeta, publish_to_es


from datetime import datetime
import os, shutil, sys
import glob
import re


mv_dir = ''

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

    quick_path = filepath.replace(PDF_DIR, '')
    product_dict['Product Type'] = quick_path.split('/')[1]

    if 'Author' in metadata:
        product_dict['Author'] = metadata['Author']
    else: 
        product_dict['Author'] = ''

    if 'Content-Type' in metadata:
        product_dict['Content Type'] = metadata['Content-Type']
    else: 
        product_dict['Content-Type'] = ''
    
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

def move_to_folder(filepath, move_dir):

    temp_dir_path = move_dir + "/" + mv_dir
    print(temp_dir_path)
    if not (os.path.exists(temp_dir_path)):
        os.system("mkdir " + temp_dir_path)
        os.system("chmod 777 " + temp_dir_path)

    os.system("mv '"+ str(filepath) +"' "+ temp_dir_path)


def process():

    global mv_dir
    mv_dir = str(datetime.now()).split()[0]

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

                move_to_folder(filepath, INGESTED_DIR)

            except Exception as e:
                print(e)
                files_on_error.append(filepath)
    
    if len(files_on_error) > 0:
        print("Error occured for files:- " + ",".join(files_on_error))
        for error_file_path in files_on_error:
            move_to_folder(error_file_path, ERROR_ON_INGESTION_DIR)
