import slate3k as slate
import PyPDF4
import numpy as np
import re
import pandas as pd


# define regex patterns to look for above and below tables

header = re.compile(r'[A-Z0-9_]+: [A-Z].*\n([a-z0-9].*)*')
header_end = re.compile(r'[a-z]')

table_start = re.compile(r'F[\n]*r[\n]*e[\n]*q[\n]*u[\n]*e[\n]*n[\n]*c[\n]*y\n%\n')
table_end = re.compile('\nT[\n]*o[\n]*t[\n]*a[\n]*l[\n]*')

def isnumeric(x):
    return x.isnumeric()


# read in a PDF
def read_pdf(filename):
    global pdfFileObj, pdfReader, npages
    pdfFileObj = open(filename, 'rb')
    extracted_text = slate.PDF(pdfFileObj)
    #pdfReader = PyPDF4.PdfFileReader(pdfFileObj)
    npages = len(extracted_text)
    dfs = []
    for page in range(npages):
        
        result = read_page(extracted_text[page])
        if result:
            (code, label), df = result
            code = code.strip().replace('\n', ' ')
            label = label.strip().replace('\n', ' ')
            if df is not None:
                df['code'] = code
                df['full_label'] = label
                dfs.append(df)
            else:
                dfs.append(pd.DataFrame.from_dict({'code': [code], 'full_label': [label]}))

    pd.concat(dfs).to_csv(filename[:-4] + '_codes.csv')

flags = ('Value', 'Label', 'Unweighted\nFrequency', '%')
def remove_extras(some_list):
    i = 0
    while i < len(some_list):
        item = some_list[i]
        if item in flags:
            some_list.pop(i)
            continue
        if len(item) < 5:
            i += 1
            
        else:
            if item[-3:] == 'xoc' or item[:5] == '• Min' or item[:5] == '• Max' \
               or item[:5] == 'Width' or item[:5] == 'Varia':
                some_list.pop(i)
            elif len(item) > 10 and item[:11] == 'Please note':
                some_list.pop(i)
            elif item[0] == '•': # pop everything until the next flag
                while some_list[i] not in flags and i < len(some_list):
                    some_list.pop(i)
                
            else:
                i += 1
    some_list.pop(-1)            

{'Value': 'short', 'Label': 'long', 'Unweighted\nFrequency': 'long', '%': 'long'}            

def read_page(text):

    first_lowercase = re.search(header_end, text)
    if first_lowercase:
        first_lowercase = first_lowercase.span()[0]
    else:
        return None
    header_text = text[:first_lowercase-1]
    
    if ':' not in header_text or len(header_text) > 200:
        return None
    header_text = header_text.split('\n')[0]
    entries = text.split('\n\n')
    if 'Value' not in entries or 'Label' not in entries:
        return header_text.split(':'), None
    
    content_start = min([entries.index(i) for i in flags])
    entries = entries[content_start:]
    pad = True
    if 'Total' not in entries:
        pad = False
    remove_extras(entries)
    n_entries = len(entries)
    if n_entries < 5:
        return header_text.split(':'), None                     

    colways_votes = []
    if n_entries > 5:
        for i in range(3, n_entries, 4):
            if '%' not in entries[i]:
                colways_votes.append(1)
            else:
                colways_votes.append(0)
    colways = round(sum(colways_votes) / len(colways_votes))
    if pad and colways:
        n_rows = int((n_entries + 1) / 4)
        entries.insert(n_rows-1, '')
        
    elif pad:
        entries.insert(-4, '')
        
        n_rows = int((n_entries+1) / 4)
    else:
        n_rows = int((n_entries) / 4)
    if colways:
        entries_grid = np.reshape(entries, (4, n_rows))
        
        entries_grid = np.flip(np.rot90(entries_grid, k=1), axis=0)
        
    else:
        entries_grid = np.reshape(entries, (n_rows, 4))
                              
    df = pd.DataFrame(entries_grid,
                  columns=['Value', 'Label', 'Frequency', 'Percent'])
    
    return header_text.split(':'), df


read_pdf('TEDS-D-2006-2014-DS0001-info-codebook.pdf')
