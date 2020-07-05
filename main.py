from service.pdf_service import process
from service.email_service import execute

import sys


def run():

    process_type = sys.argv[1]

    if not process_type:
        print("Process name is required. Please provide either email or pdf")

    if process_type == "pdf": process

    if process_type == "email": execute


run()