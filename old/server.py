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
from random import randint

app = Flask(__name__)
ix = index.open_dir(INDEX_DIR)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

@app.route('/')
def start():
    not_found = request.args.get('not_found', '')
    q = request.args.get('q', '')
    return render_template("index.html", results=query(q), query=q, rand_emoji=rand_emoji())

@app.route('/emoji/<index>')
def emojis(index):
    return render_template("single.html", emoji=get_emoji(index))
    

def query(querystring):
    parser = MultifieldParser(["name", "annotations", "description", "related_to", "known_as"], ix.schema, termclass=Variations)
    myquery = parser.parse(querystring)
    searcher = ix.searcher()
    return searcher.search(myquery)

def get_emoji(index):
    try:
        with open(join(DOCUMENT_FOLDER, index)) as document:
            emoji = pickle.load(document)
            return emoji
    except IOError, e:
        return redirect(url_for('start', not_found=1))

def rand_emoji():
    rand = randint(1, 1281)
    return get_emoji(str(rand))

if __name__ == '__main__':
    app.debug = True
    app.run()