from flask import Flask, jsonify, current_app
import test2
import json


app = Flask(__name__)


@app.route('/')
def hello_world():
    return current_app.send_static_file('layout.html')

@app.route('/search/<searchterm>')
def search(searchterm):

    search_results = test2.search(searchterm)
    message = {
        'status': 200,
        'message': 'OK',
        'scores': search_results
    }
    col = []

    original = search_results['original_results']

    for i, j in original[0].items():
        titDesc = test2.titleDesc(i, original[1])
        test = {}
        test["page"] = i
        test["title"] = titDesc[0]
        test["desc"] = titDesc[1]
        test["value"] = j
        test["resultType"] = "original"
        col.append(test)

    if 'new_results' in search_results.keys():
        new = search_results['new_results']

        for i, j in new[0].items():
            titDesc = test2.titleDesc(i, new[1])
            test = {}
            test["page"] = i
            test["title"] = titDesc[0]
            test["desc"] = titDesc[1]
            test["value"] = j
            test["resultType"] = "new"
            col.append(test)

    if 'intersection' in search_results.keys():
        intersection = search_results['intersection']

        for i, j in new[0].items():
            titDesc = test2.titleDesc(i, new[1])
            test = {}
            test["page"] = i
            test["title"] = titDesc[0]
            test["desc"] = titDesc[1]
            test["value"] = j
            test["resultType"] = "intersection"
            col.append(test)


    tmp = json.dumps(col)
    if 'new_results' in search_results.keys():
        tmp1 = {
            'results': tmp,
            'new_keywords': new[1]
        }
    else:
        tmp1 = {
            'results': tmp
        }
    return jsonify(tmp1)


@app.route('/<path:path>')
def static_proxy(path):
  return app.send_static_file(path)

if __name__ == '__main__':
    app.run()
