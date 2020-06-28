
ROOT_DIR = ""
PDF_DIR = ROOT_DIR + "/data"
INGESTED_DIR = ROOT_DIR + "/ingested_data"
ERROR_ON_INGESTION_DIR = ROOT_DIR + "/error_on_ingestion"


ELASTICSEARCH = {
    "URL": "http://localhost:9200",
    "INDEX": "test",
    "DOC_TYPE": "pdf",
    "TIMEOUT": 10
}
TIKA_SERVER = {
    "URL": "http://localhost:9998/tika",
    "HEADERS": {
        'Content-type': 'application/pdf'
    },
    "TIMEOUT": 10
}
