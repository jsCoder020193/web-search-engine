from flask import Flask, jsonify, current_app
import test2
import json


app = Flask(__name__)


@app.route('/')
def hello_world():
    return current_app.send_static_file('layout.html')

@app.route('/search/')
@app.route('/search/<searchterm>')
'''def search(searchterm = None):
    if searchterm == None:
        tmp = '[]'
        return jsonify(tmp)
    if(searchterm[0] == '"'):
        # Phrasal Search
        results = test2.phrasal_search(searchterm)
    else:
        results = test2.cosine(searchterm)'''

#added code here
def search(searchterm):
    if(searchterm[0] == '"'):
        # Phrasal Search
        # results = test2.phrasal_search(searchterm)
        results, words = test2.phrasal_search(searchterm)

    else:
        results, words = test2.cosine(searchterm)

    message = {
        'status': 200,
        'message': 'OK',
        'scores': results
    }
    col = []

    for i,j in results.items():
        titDesc=test2.titleDesc(i,words)
        test = {}
        test["page"] = i
        test["title"]= titDesc[0]
        test["desc"]= titDesc[1]
        test["value"] = j
        col.append(test)

   
    tmp = json.dumps(col)
    return jsonify(tmp)


@app.route('/<path:path>')
def static_proxy(path):
  # send_static_file will guess the correct MIME type
  return app.send_static_file(path)

if __name__ == '__main__':
    app.run()
