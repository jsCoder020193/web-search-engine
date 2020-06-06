
import re
import zipfile
from collections import Counter, OrderedDict
from math import log2,sqrt

archive= zipfile.ZipFile('Jan.zip','r')

files= archive.namelist()

N = len(files)

# terms = Counter()
documents= {}
positions= {}
terms ={}
df= {} #document frequency
tfidf = {}

for i in files:
    file= archive.open(i,'r')
    words= str(ascii(file.read()))
    words = re.sub('<[^>]*>', "  ", words)
    words = re.sub('[\s+|\\n]', " ", words)
    words = re.sub('\{[^}]*\}', " ", words)
    words = re.sub('[^\w]', " ", words)
    words = re.sub(' +', " ", words)
    words = re.sub('\b[an|the|and|is|for|a|its|it\'s|on]*\b', "", words)
    words = re.sub(r'\b\w{1,2}\b', '', words)
    words = words.lower()
    wordlist= words.split()
    # terms = []
    terms ={}

    #index = position w= word
    for index, word in enumerate(wordlist):
        if(word in terms):
            terms[word][0] +=1
            terms[word][1].append(index)
        else:
            terms[word]= [1,[index]]
            if word in df:
                df[word].append(i)
            else:
                df[word] = []
                df[word].append(i)


    documents[i]= terms
    c= ""

print(df)
for i in files:
    fterms = documents[i]
    tmax = max(fterms.values())[0]

    for term,value in fterms.items():
        tf = value[0]/tmax  #freq of term in doc/max freq
        idf = log2(N/(len(df[term])+1)) + 1 #Smoothed idf
        tfidf[i,term] = tf*idf

while c != "exit":
    c = input("Input keyword:")
    arr= []
    for doc in documents:
        if c in documents[doc]:
            arr.append(doc)
    print("Files containing " + c + " :")
    print(arr)

