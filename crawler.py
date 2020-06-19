import re
import zipfile
from collections import Counter, OrderedDict
from math import log2,sqrt
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize
from bs4 import BeautifulSoup, Comment
import ntpath
import nltk
import os
import chardet


archive= zipfile.ZipFile('rhf.zip','r')


extensions = ('.htm', '.html')
files = []
urlsProcessed = {}
anchorText= {}


def buildUrls(url):
    queue = [ url ]
    while len(queue) > 0:
        url = queue.pop(0)
        if url in urlsProcessed:
            continue
        urlsProcessed[url]=1
        head, tail = ntpath.split(url)
        try:
            file= archive.read(url)
        except :
            print(url)
            continue
        soup = BeautifulSoup(file, 'html.parser')
        links = soup.find_all('a', attrs={'href': re.compile("html|htm$")})

        for link in links:
            if link['href'].endswith('html') == False:
                continue
            if  link['href'].startswith(head):
                if link['href'] not in urlsProcessed :
                    anchorText[url]= link.get_text(strip=True)
                    queue.append(link['href'])
            elif '../' in link['href']:
                continue
            else:
                url = head + "/" + link['href']
                if url not in urlsProcessed:
                    anchorText[url] = link.get_text(strip=True)
                    queue.append(url)

        

buildUrls('rhf/index.html')
print("Done")
print("Files Processed " + str(len(urlsProcessed)))