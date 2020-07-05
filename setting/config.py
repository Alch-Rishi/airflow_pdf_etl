
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
    "TIMEOUT": 10,
    "PREV_DAYS": 7
}
TIKA_SERVER = {
    "URL":"http://tikaserver:9998",

    "CONTENT_HEADERS": {
        "Content-type": "application/pdf"
    },
   "META_HEADERS": { 
        "Accept": "application/json"
    },

    "TIMEOUT": 120
}

SMTP_SERVER = {
    "SUBJECT": "Ingestion Email",
    "HOST":"smtp.gmail.com",
    "PORT":587,
    "FROM":"tika.test.app@gmail.com",
    "USERNAME":"tika.test.app@gmail.com",
    "PASSWORD":"tikatest123",
    "TO":["tika.test.app@gmail.com"]
}
#tika.etl.test@gmail.com
