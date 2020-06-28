
ROOT_DIR = "/root/airflow_perosnal/airflow_pdf_etl"
# PDF_DIR = ROOT_DIR + "/data"
PDF_DIR = "/root/test"
INGESTED_DIR = ROOT_DIR + "/ingested_data"
ERROR_ON_INGESTION_DIR = ROOT_DIR + "/error_on_ingestion"


ELASTICSEARCH = {
    "URL": "http://localhost:9200",
    "INDEX": "test",
    "DOC_TYPE": "pdf",
    "TIMEOUT": 10
}
TIKA_SERVER = {
    "URL":"http://localhost:9998",

    "CONTENT_HEADERS": {
        'Content-type': 'application/pdf'
    },
   "META_HEADERS": { 
        'Content-type': 'application/json'
    },

    "TIMEOUT": 10
}
