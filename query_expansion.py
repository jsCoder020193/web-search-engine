import pickle
import os

documents= pickle.load( open( "documents.p", "rb" ) )
tfidf = pickle.load( open( "tfidf.p", "rb" ) )

def WriteDictToCSV(csv_file,file_type,dict_data):
    try:
        with open(csv_file, 'w') as f:
            if file_type == 'txt':
                for item in dict_data:
                    f.write("%s\n"%str(item))
            elif file_type == 'dict':
                for key in dict_data.keys():
                    f.write("%s,%s\n"%(key,dict_data[key]))
        f.close()
    except IOError as e:
        errno, strerror = e.args
        print("I/O error({0}): {1}".format(errno,strerror))
    return

def sort_dict(x):
    return {k: v for k, v in sorted(x.items(), key=lambda item: item[1],reverse=True)}

def first_five_keys(x):
    # return {k: x[k] for k in list(x)[:5]}
    return list(x.keys())[:5]

def correlation_matrix(cosine_sim, words):
    cosine_sim = sort_dict(cosine_sim)
    A = first_five_keys(cosine_sim)
    k = [list(documents[x].keys()) for x in A]
    terms = list(set(item for sublist in k for item in sublist))

    correlation_matrix = {}
    for w in words:
        for term in terms:
            sum = 0
            for doc in A:
                prod = 0
                if((doc,term) in tfidf.keys()) and ((doc,w) in tfidf.keys()):
                    prod = tfidf[doc,term]*tfidf[doc,w]
                sum +=prod
            # if not(w == term): #Ignoring original keywords as they will have max correlation by default
            correlation_matrix[w,term] = sum
    correlation_matrix = sort_dict(correlation_matrix)
    correlation_matrix = first_five_keys(correlation_matrix)
    new_words = [x[1] for x in correlation_matrix] + words
    unique_words = set(new_words) 
    new_query = ''
    for x in unique_words:
        new_query+=x+' '
    new_query = new_query.strip()

    return new_query
