import flask
from flask import request, jsonify
from flask_cors import CORS


# from gensim.models.wrappers import FastText
from gensim.models import KeyedVectors

# model = FastText.load_fasttext_format('id.bin')
model = KeyedVectors.load_word2vec_format('id.vec')

app = flask.Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.config["DEBUG"] = True

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@app.route('/similar', methods=['GET'])
def get_similar():
    key = request.args.get('key')
    similar =  model.similar_by_word(key, 100)

    response = []
    result = []
    outcome = []
    count = 0

    for i, j in similar:
        if count<10:
            for line in open('quran.txt'):
                if i in line:
                    outcome.append(line.strip())

            if outcome:
                count+=1
                result.append(i)

            outcome.clear()

    for i in result:
        response.append({'value':i})

    return jsonify(response)

@app.route('/translation', methods=['GET'])
def get_translation():
    result = []
    response = []
    similar = []
    key = request.args.get('key')
    for line in open('quran.txt'):
        if key in line:
            result.append(line.strip())

    if result:
        for item in result:
            output = item.split('|')
            response.append(output)

        list_translation = []
        for i, j, k in response:
            list_translation.append({'surah':i, 'ayat':j, 'text':k})
        return jsonify(list_translation)
    else:
        return jsonify({"message":"Data not found"})

app.run(port=4000)