from flask import Flask, jsonify, current_app
import test2
import json


app = Flask(__name__)


@app.route('/')
def hello_world():
    return current_app.send_static_file('layout.html')

@app.route('/search/<searchterm>')
def search(searchterm):
    if(searchterm[0] == '"'):
        # Phrasal Search
        results = test2.phrasal_search(searchterm)
    else:
        results = test2.cosine(searchterm)
    message = {
        'status': 200,
        'message': 'OK',
        'scores': results
    }
    col = []

    for i,j in results.items():
        titDesc=test2.titleDesc(i,searchterm)
        test = {}
        test["page"] = i
        test["title"]= titDesc[0]
        test["desc"]= titDesc[1]
        test["value"] = j
        col.append(test)

   
    tmp = json.dumps(col)
    return jsonify(tmp)


if __name__ == '__main__':
    app.run()
