
import re
import zipfile
from collections import Counter, OrderedDict
from math import log2,sqrt
from nltk.corpus import wordnet
from bs4 import BeautifulSoup, Comment
import chardet
import os

archive= zipfile.ZipFile('rhf.zip','r')

if not(os.path.isdir("./static/rhf")):
    archive.extractall('./static/')

extensions = ('.htm', '.html')
files = []
[files.append(file) for file in archive.namelist() if file.endswith(extensions)]

N = len(files)

print(N)
# terms = Counter()
documents= {}
positions= {}
terms ={}
df= {} #document frequency
tfidf = {}
doc_len= {}
title_desc={}
url= {}

for i in files:
    
    # try:
    #     file_contents = archive.read(i).decode('cp1252')
    # except:
    #     file_contents = archive.read(i).decode('ascii')
    # file_contents = archive.read(i)
    file_contents = archive.open(i,'r')

    # encoding = chardet.detect(file_contents)['encoding']
    # print(encoding)
    # try:
    #     file_contents.decode(encoding, errors='ignore')
    # except:
        # pass
    soup = BeautifulSoup(file_contents, 'html.parser')

    # if soup.find('title'):
    #     title = soup.find('title').text
    # else:
    #     title=""
    # title_desc[i]= [title, ""]

    # url[i] = []
    # for a in soup.find_all('a', attrs={'href': re.compile("html|htm$")}):
    #     url[i].append([a['href'],a.string])
    # path = zipfile.Path(i, at='')
    # print(path)
    