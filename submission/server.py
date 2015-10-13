"""
server.py
---------

Author: Richard Luong

Starts the web server.
"""

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import whoosh.index as index
from whoosh.query import Variations
from whoosh.qparser import MultifieldParser
from os.path import join
import pickle
from constants import DOCUMENT_FOLDER
from constants import INDEX_DIR

import sys
import logging
from random import randint

app = Flask(__name__)
ix = index.open_dir(INDEX_DIR)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

NUM_EMOJI = 1281

@app.route('/')
def start():
    """Index page"""
    querystring = request.args.get('q', '')
    return render_template("index.html",
                           results=query(querystring),
                           query=querystring,
                           rand_emoji=rand_emoji())

@app.route('/emoji/<emoji_index>')
def emojis(emoji_index):
    """
    Single page for every emoji.

    Parameters:
    -----------
    emoji_index - index of the emoji
    """
    return render_template("single.html", emoji=get_emoji(emoji_index))

def query(querystring):
    """
    Parse, queries the query string from the user.
    Returns a list of emojis.

    Parameters:
    -----------
    querystring - the query string from the user

    Return:
    -------
    list - list of results (can be empty)
    """
    parser = MultifieldParser(["name", "annotations", "description", "related_to", "known_as"],
                              ix.schema,
                              termclass=Variations)
    myquery = parser.parse(querystring)
    searcher = ix.searcher()
    return searcher.search(myquery)

def get_emoji(emoji_index):
    """
    Returns a emoji object from the specificed emoji_index

    Parameters:
    -----------
    emoji_index - index of the emoji

    Return:
    -------
    emoji - a emoji object corresponding to the index
    """
    try:
        with open(join(DOCUMENT_FOLDER, emoji_index)) as document:
            emoji = pickle.load(document)
            return emoji
    except IOError, error:
        return redirect(url_for('start'))

def rand_emoji():
    """Returns a random emoji."""
    rand = randint(1, NUM_EMOJI)
    return get_emoji(str(rand))

if __name__ == '__main__':
    app.debug = True
    app.run()
