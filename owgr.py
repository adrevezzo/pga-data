import os
import re
from PyPDF2 import PdfReader

def read_pdf(pdf_file):
    text = ''
    raw_text = []
    with open(pdf_file, "rb") as file:
        pdf = PdfReader(file)
        for page in pdf.pages:
            raw_text.append(page.extract_text().split())
   
    return raw_text

print(read_pdf('owgr_pdfs/owgr01f2013.pdf'))

# print(os.listdir('owgr_pdfs'))

old_format_pattern = re.compile(r'^(?P<year>[0-9]{4})_(?P<week>[0-9]{2})OWGR(?P<pdf_ext>\.pdf$)')
matches = []

folder = 'owgr_pdfs'
out_folder = 'test'
for filename in os.listdir(folder):
    # os.rename()
    file_match = old_format_pattern.search(filename)
    if file_match:
        # matches.append((file_match.group('year'),file_match.group('week') ))
        dst = f"owgr{file_match.group('week')}f{file_match.group('year')}.pdf"
        src = f"{folder}/{filename}"
        dst = f"{folder}/{dst}"
        os.rename(src, dst)



