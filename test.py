from service.pdf_service import process
from service.email_service import execute


## Triggering parse process
print("\n\n\n\n-------------PDF SERVICE START---------------")
process()
print("\n\n-------------PDF SERVICE Finish---------------")

print("\n\n\n\n-------------EMAIL SERVICE START---------------")
execute()
print("\n\n-------------PDF SERVICE Finish---------------")