
ROOT_DIR = "/usr/local/etl/"
PDF_DIR = ROOT_DIR + "/data"
# PDF_DIR = "/root/test"
INGESTED_DIR = ROOT_DIR + "/ingested_data"
ERROR_ON_INGESTION_DIR = ROOT_DIR + "/error_on_ingestion"
ELASTICSEARCH = {
    "URL": "http://elasticsearch:9200",
    "HEADERS": {
        "Content-type": "application/json"
    },
    "INDEX": "test",
    "DOC_TYPE": "pdf",
    "TIMEOUT": 10
}
TIKA_SERVER = {
    "URL":"http://tikaserver:9998",

    "CONTENT_HEADERS": {
        "Content-type": "application/pdf"
    },
   "META_HEADERS": { 
        "Accept": "application/json"
    },

    "TIMEOUT": 10
}
