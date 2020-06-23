import zipfile
import pickle
import os
import numpy as np
from tabulate import tabulate
from test2 import cosine_sim

archive= zipfile.ZipFile('rhf.zip','r')

if not(os.path.isdir("./static/rhf")):
    archive.extractall('./static/')

extensions = ('.htm', '.html')
files = []
[files.append(file) for file in archive.namelist() if file.endswith(extensions)]

N = len(files)

urlsProcessed = pickle.load( open( "urlsProcessed.p", "rb" ) )
anchorText= pickle.load( open( "anchorText.p", "rb" ) )
documents= pickle.load( open( "documents.p", "rb" ) )
positions= pickle.load( open( "positions.p", "rb" ) )
terms =pickle.load( open( "terms.p", "rb" ) )
df= pickle.load( open( "df.p", "rb" ) )
tfidf = pickle.load( open( "tfidf.p", "rb" ) )
doc_len= pickle.load( open( "doc_len.p", "rb" ) )

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

currentPath = os.getcwd()

def normalized_association_matrix():
    doc_keys = np.unique([element[0] for element in tfidf.keys()])
    term_keys = np.unique([element[1] for element in tfidf.keys()])

    association_matrix = {}

    # for ti in term_keys:
    #     for tj in term_keys:
    #         sum = 0
    #         for d in doc_keys:
    #             sum += tfidf[d][ti] * tfidf[d][tj] 
    #         association_matrix[ti,tj] = sum


    WriteDictToCSV(currentPath + "/csv/tfidf_table.csv",'dict',association_matrix)
    # WriteDictToCSV(currentPath + "/csv/tfidf_table.txt",tabulate(np.dot(tfidf.transpose(),tfidf), tablefmt='grid'))


    # return cosine_sim

# WriteDictToCSV(currentPath + "/csv/documents.csv",{key:documents[key] for key in list(documents.keys())[:250]})
normalized_association_matrix()
print("Done")
print("Files Processed " + str(len(documents)))
