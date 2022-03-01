import csv
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdocument import PDFDocument
from pdfminer.layout import LAParams
from pdfminer.converter import TextConverter
from io import StringIO
import os
import re
import PyPDF2


def get_cv_email(cv_path):
    text = convert_pdf_to_string(cv_path)
    match = re.search(
        # [a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$
        # [\w\.-]+@[\w\.-]+
        # \w+(?:[.-]\w+)*@\w+(?:[.-]\w+)+[.-][a-z_0-9]+(?=[A-Z]|(?!=[.-])\b)
        r'[\w\.-]+@[\w\.-]+',
        text)

    try:
        return match.group(0)
    except:
        print("An exception occurred")


def pdf_to_txt():
    pdfFileObject = open(
        r"/Users/OpenMindes/Dev/python/pdfs/src/amine-benkadi-cv.pdf", 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
    print(" No. Of Pages :", pdfReader.documentInfo)
    pageObject = pdfReader.getPage(0)
    print(pageObject.extractText())
    pdfFileObject.close()


def convert_pdf_to_string(file_path):

    output_string = StringIO()
    with open(file_path, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)

    return(output_string.getvalue())


def convert_title_to_filename(title):
    filename = title.lower()
    filename = filename.replace(' ', '_')
    return filename


def split_to_title_and_pagenum(table_of_contents_entry):
    title_and_pagenum = table_of_contents_entry.strip()

    title = None
    pagenum = None

    if len(title_and_pagenum) > 0:
        if title_and_pagenum[-1].isdigit():
            i = -2
            while title_and_pagenum[i].isdigit():
                i -= 1

            title = title_and_pagenum[:i].strip()
            pagenum = int(title_and_pagenum[i:].strip())

    return title, pagenum


def get_pdfs_list():
    path = '/Users/OpenMindes/Dev/python/pdfs/src/'
    folder = os.fsencode(path)
    filenames = []
    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        # whatever file types you're using...
        if filename.endswith(('.pdf', '.jpeg', '.png')):
            filenames.append(filename)

    filenames.sort()
    print(filenames)
    return filenames


pdfs = get_pdfs_list()
for pdf in pdfs:
    print(get_cv_email(cv_path=f'./{pdf}'))
