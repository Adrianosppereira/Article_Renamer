import sys
import requests
import PyPDF2
from glob import glob
import os
import shutil

crossref = 'http://api.crossref.org/'

if __name__ == '__main__':
    dr = os.getcwd() ## Get directory 
    nRenamedArticles = 0
    files = glob(os.path.join(dr, "*.pdf"))
    nFiles = len(files) ## Lenght of list equal to total number of selected files
    for pdf in files:
        pdfReader = PyPDF2.PdfFileReader(pdf, strict=False)
        if pdfReader.isEncrypted:
            # print (pdf)
            continue

        title = None
        year = None
        doi = None

        for k, v in pdfReader.documentInfo.items():
            if 'doi' in k.lower(): ## Get doi from metadata (for when it is properly registered)
                doi = v
            if not doi and 'doi:' in v.lower(): ## Get doi from metadata (for when they filled the wrong field)
                    doi = v.replace('doi:','')
            if not doi and 'doi ' in v.lower(): ## Get doi from metadata (for when they filled the wrong field)
                    doi = v.replace('doi ','')
            if not doi: ## Get desperate and try to get the doi from the text in the .pdf file
                ## Read the number of pages
                numberOfPages = pdfReader.getNumPages()
                ## Register text from page 1
                text_in_file = pdfReader.getPage(0).extractText().lower()
                if numberOfPages > 1: ## Register text from page 2
                    text_in_file = text_in_file + ' ' + pdfReader.getPage(1).extractText().lower()
                if numberOfPages > 5 and 'doi' not in text_in_file: ## Register text from page 3-6, aiming to get the doi of books
                    text_in_file = text_in_file + ' ' + pdfReader.getPage(2).extractText().lower() + ' ' + pdfReader.getPage(3).extractText().lower() + ' ' + pdfReader.getPage(4).extractText().lower()+ ' ' + pdfReader.getPage(5).extractText().lower()
                ## Clean registered text and isolate 'doi*code'
                text_in_file = text_in_file.replace('\n', ' ').replace('correspondingauthor', ' ').replace('contentslistsavailable', ' ').replace(']', ' ').replace('[', ' ').replace('©', ' ')
                ## Extract the actual doi from 'doi*code' 
                if 'doi:' in text_in_file:
                    doi_index_start = text_in_file.find('doi:')
                    doi_index_end = text_in_file.find(' ', doi_index_start) 
                    DIO = text_in_file[slice(doi_index_start+4,doi_index_end)]
                    if DIO.startswith('10'):
                        # print('DIOOO = ' + DIO)
                        doi = DIO
                if not doi and 'doi.org/' in text_in_file:
                    doi_index_start = text_in_file.find('doi.org/')
                    doi_index_end = text_in_file.find(' ', doi_index_start) 
                    DIO = text_in_file[slice(doi_index_start+8,doi_index_end)]
                    if DIO.startswith('10'):
                        # print('DIOOO = ' + DIO)
                        doi = DIO   
                if not doi and 'doi' in text_in_file:
                    doi_index_start = text_in_file.find('doi')
                    doi_index_end = text_in_file.find(' ', doi_index_start) 
                    DIO = text_in_file[slice(doi_index_start+3,doi_index_end)]
                    if DIO.startswith('10'):
                        # print('DIOOO = ' + DIO)
                        doi = DIO                   
            if not doi and 'title' in k.lower(): ## Assume that somehow they properly filled the title field in the metadata 
                title = v
                
        if doi: ## Use acquired doi to get document info from the web
            try:
                url = '{}works/{}'.format(crossref, doi)
                r = requests.get(url)
                item = r.json()
                year = item['message']['created']['date-parts'][0][0]
                title = item['message']['title'][0]
            except ValueError:  # (╯°□°)╯︵ ┻━┻ Give up from current file if acquired doi is invalid or if website does not return usefull data
                continue

        ## Name format: title, year.pdf
        name = None
          
        if title and not title.isspace() and len(title.split(' '))>=2:
            name = title.replace(':', " -").replace('/','-').replace('?','').replace('&','and') ## Assign name while cleanning title of invalid characters
            remaining_lenght = 240 - len(dr) - len('.pdf') ## Crop name string to fit MAX_LENGHT
            if  len(name) > remaining_lenght:
                name = name[0:remaining_lenght]
            if year:
                name = name+', '+str(year)
        
        if name: ## Rename file
            filename = os.path.join(dr, str(name)) + '.pdf'
            if os.path.exists(filename):
                filename = filename.replace('.pdf', '-RPT.pdf') ## If file already exists add -RPT to file name
            shutil.move(pdf, filename)
            nRenamedArticles = nRenamedArticles + 1 ## Counter for the number of renamed files
            
    print('DONE!')
    print(f'{nRenamedArticles} out of {nFiles} .pdf files were renamed')

## by Adriano.s.p.p and Denise.a.g - 09/07/2020; inpired by NECESSITY and "Pu Du" from https://www.researchgate.net/post/What_is_the_best_way_to_rename_a_collection_of_academic_papers
