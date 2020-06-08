
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
    #removes \\n
    words = re.sub(r"\\n", " ", words)
    #removes apostrophe joins word \\\' 
    words = re.sub(r"\\\'", "", words)
    #removes special character and keeps a-z0-9
    words = re.sub('[^\w]', " ", words)
    #removes extra space    
    words = re.sub(' +', " ", words)
    words = re.sub('\b[an|the|and|is|for|a|its|it\'s|on]*\b', "", words)
    words = re.sub(r'\b\w{1,2}\b', '', words)
    #remove extra spaces after removal of 2 letter words
    words = re.sub(' +', " ", words)
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

for i in files:
    fterms = documents[i]
    tmax = max(fterms.values())[0]

    #added doc_sum
    doc_sum = 0
    for term,value in fterms.items():
        tf = value[0]/tmax  #freq of term in doc/max freq
        idf = log2(N/(len(df[term])+1)) + 1 #Smoothed idf
        tfidf[i,term] = tf*idf
        #doc_sum hold all tfidf for a document and squares them
        doc_sum = doc_sum + ((tf*idf) ** 2)
        #doc_length is the sqrt of the document sum
        doc_length = sqrt(doc_sum)
    #Test print
    #print(i,":",sqrt(doc_sum))
    #print(i,":",doc_length)        
    
#added his print from his example here
print("Now the search begins:")

c= "none"
while c != "":
    c = input("enter a search key=>")
    arr= []
    for doc in documents:
        if c in documents[doc]:
            arr.append(doc)
    if len(arr)>0:
        print("found a match:")
        print(arr)
    else:
        if c!="":
            print("no match")
        else:
            print("Bye")
