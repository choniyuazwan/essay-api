import flask
from flask import request, jsonify
import sqlite3

# from gensim.models.wrappers import FastText
from gensim.models import KeyedVectors

# model = FastText.load_fasttext_format('id.bin')
model = KeyedVectors.load_word2vec_format('id.vec')

app = flask.Flask(__name__)
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
    word = request.args.get('key')
    similar_words =  model.similar_by_word(word)

    response = []
    for i, j in similar_words:
        response.append({'word':i, 'value':j})

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

# @app.route('/translation', methods=['GET'])
# def get_translation():
#     result = []
#     response = []
#     similar = []
#     key = request.args.get('key')
#     for line in open('quran.txt'):
#         if key in line:
#             result.append(line.strip())

#     if not result:
#         similar = model.similar_by_word(key)
        
#         response = []
#         for i, j in similar:
#             response.append({'word':i, 'value':j})

#         return jsonify(response)
#     else:
#         for item in result:
#             output = item.split('|')
#             response.append(output)

#         list_translation = []
#         for i, j, k in response:
#             list_translation.append({'surah':i, 'ayat':j, 'text':k})
#         return jsonify(list_translation)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM books;').fetchall()

    return jsonify(all_books)


@app.route('/api/v1/resources/books', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')

    query = "SELECT * FROM books WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    if not (id or published or author):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

app.run(port=4000)