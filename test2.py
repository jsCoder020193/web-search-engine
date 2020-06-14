
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
doc_len= {}
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
    doc_len[i] = sqrt(doc_sum)

#Parse Query and get documents belonging to all the keywords
def queryParser(query):
    str = query
    docs = []
    operator = ""
    #Check for and or and but
    if "and" in str:
        operator = "and"
        str = list(filter(("and").__ne__, str)) #revoming the word and from the list.
    elif "or" in str:
        operator = "or"
        str = list(filter(("or").__ne__, str))
    elif "but" in str:
        operator = "but"
        str = list(filter(("but").__ne__, str))
    else:
        operator = "none"

    #Do Query operations and retrieve list of documents belong to the keywords.
    if str:
        if str[0] in df.keys():
            docs = df[str[0]]
        for d in str:
            if d in df.keys() and operator == "none":
                docs = list(set(df[d]) & set(docs))
            elif d in df.keys() and operator == "and":
                docs = list(set(df[d]) & set(docs))
            elif d in df.keys() and operator == "or":
                docs = list(set(df[d]) | set(docs))
            elif d in df.keys() and operator == "but":
                docs = list(set(docs) - set(df[d]))

    return docs


def cosine(keywords):
    cosine_sim = {}
    str = keywords.lower().split()
    docs = queryParser(str)
            
    inner = Counter()
    for x in docs:
        for tf in str:
           inner[x] += tfidf[x,tf]
        cosine_sim[x]= inner[x] /(doc_len[x]*sqrt(len(str)))
    return cosine_sim
    

# def phrasal_search(keywords):

c= "none"
while c != "":
    c = input("enter a search key=>")
    c = re.sub('"','', c )
    k = c.split( )
    and_docs = list(cosine(c).keys())
    # for x in k:
    #     if x in df.keys():
    #         docs = df[x]
    #     # f = cosine(x).keys()
    #     # for i in f:
    #         if len(and_docs) == 0:
    #             and_docs.append(docs)
    #         else:
    #             print(list(set(and_docs) & set(docs)))
    #             and_docs.append("1")

    R = []

    for doc in and_docs:
        current_doc_terms = documents[doc]
        # Positions of k0
        g = current_doc_terms[k[0]]
        # For each position p of keyword k_0 in P_0(g)
        match_found = 1
        for p in g[1]:
            # For each keyword k_j, 1≤j ≤m
            for idx, j in enumerate(k[1:]):
                # Check whether p+|k_(j-1) |+1∈P_j
                pj_doc = current_doc_terms[j]
                pj = pj_doc[1]
                # p + len(k[idx]) + 1
                if (p + idx+ 1) not in pj:
                    match_found = 0

        if(match_found == 1):
            R.append(doc)

    if len(R)>0:
        print("found a match:")
        print(R)
    else:
        if c!="":
            print("no match")
        else:
            print("Bye")


    #Test print
    #print(i,":",sqrt(doc_sum))
    #print(i,":",doc_length)        
    
#added his print from his example here
# print("Now the search begins:")
#
# c= "none"
# while c != "":
#     c = input("enter a search key=>")
#     arr= []
#     for doc in documents:
#         if c in documents[doc]:
#             arr.append(doc)
#     if len(arr)>0:
#         print("found a match:")
#         print(arr)
#     else:
#         if c!="":
#             print("no match")
#         else:
#             print("Bye")
