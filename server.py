from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import whoosh.index as index
from whoosh.query import Variations
from whoosh.qparser import MultifieldParser

from os.path import isfile, join
import pickle

from constants import DOCUMENT_FOLDER, INDEX_DIR

import sys
import logging

app = Flask(__name__)
ix = index.open_dir(INDEX_DIR)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

@app.route('/')
def start():
    not_found = request.args.get('not_found', '')
    q = request.args.get('q', '')
    if q == "":
        return render_template('index.html')
    else:
        return render_template("index.html", results=query(q), query=q)

@app.route('/emoji/<index>')
def emojis(index):
    try:
        with open(join(DOCUMENT_FOLDER, index)) as document:
            emoji = pickle.load(document)
        return render_template("single.html", emoji=emoji)
    except IOError, e:
        return redirect(url_for('start', not_found=1))

def query(querystring):
    parser = MultifieldParser(["name", "annotations", "description", "related_to", "known_as"], ix.schema, termclass=Variations)
    myquery = parser.parse(querystring)
    searcher = ix.searcher()
    return searcher.search(myquery)

if __name__ == '__main__':
    app.run()