import sys
import requests
import PyPDF2
from glob import glob
import os
import shutil

crossref = 'http://api.crossref.org/'

if __name__ == '__main__':
    dr = os.getcwd()
    for pdf in glob(os.path.join(dr, "*.pdf")):
        pdfReader = PyPDF2.PdfFileReader(pdf, strict=False)
        if pdfReader.isEncrypted:
            # print (pdf)
            continue

        title = None
        year = None
        doi = None

        for k, v in pdfReader.documentInfo.items():
            if 'doi' in k.lower():
                doi = v
            if not doi and 'doi:' in v.lower():
                    doi = v.replace('doi:','')
            if not doi:
                text_in_file = pdfReader.getPage(0).extractText().lower()
                if pdfReader.getNumPages() > 1:
                    text_in_file = text_in_file + ' ' + pdfReader.getPage(1).extractText().lower()
                text_in_file = text_in_file.replace('\n', ' ').replace('correspondingauthor', ' ').replace('contentslistsavailable', ' ').replace(']', ' ').replace('[', ' ')
                if 'doi:' in text_in_file:
                    doi_index_start = text_in_file.find('doi:')
                    doi_index_end = text_in_file.find(' ', doi_index_start) 
                    DIO = text_in_file[slice(doi_index_start+4,doi_index_end)]
                    if DIO.startswith('10'):
                        # print(DIO)
                        doi = DIO
            if not doi and 'title' in k.lower():
                title = v
                
        if doi:
            try:
                url = '{}works/{}'.format(crossref, doi)
                r = requests.get(url)
                item = r.json()
                year = item['message']['created']['date-parts'][0][0]
                title = item['message']['title'][0]
            except ValueError:  # (╯°□°)╯︵ ┻━┻
                continue

        # format: title, year.pdf
        name = None
          
        if title and not title.isspace() and len(title.split(' '))>=2:
            name = title.replace(':', " -").replace('/','-').replace('?','').replace('&','and')
            remaining_lenght = 240 - len(dr) - len('.pdf')
            if  len(name) > remaining_lenght:
                name = name[0:remaining_lenght]
            if year:
                name = name+', '+str(year)
        
        if name:
            filename = os.path.join(dr, str(name)) + '.pdf'
            if os.path.exists(filename):
                filename = filename.replace('.pdf', '-RPT.pdf')
            shutil.move(pdf, filename)
    print('DONE!')

## by Denise.a.g and Adriano.s.p.p - 16/06/2020
## for V2 maybe use the pdftotext library instead PyPDF2 and focus in getting text out of the more annoying pdfs.
