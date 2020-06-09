from flask import Flask, jsonify, current_app
import test2
import json


app = Flask(__name__)


@app.route('/')
def hello_world():
    return current_app.send_static_file('search.html')

@app.route('/search/<searchterm>')
def search(searchterm):
    results = test2.cosine(searchterm)
    message = {
        'status': 200,
        'message': 'OK',
        'scores': results
    }
    col = []

    for i,j in results.items():
        test = {}
        test["page"] = i
        test["value"] = j
        col.append(test)

   
    tmp = json.dumps(col)
    return jsonify(tmp)


if __name__ == '__main__':
    app.run()
