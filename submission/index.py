"""
index.py
--------

Author: Richard Luong

Indexes the documents in DOCUMENT_FOLDER
"""

import pickle
import os

from constants import DOCUMENT_FOLDER
from constants import INDEX_DIR
from os.path import isfile
from os.path import join
from whoosh.index import create_in
from whoosh.fields import ID, TEXT, KEYWORD, STORED, Schema
from whoosh.analysis import StemmingAnalyzer

def load_emojis():
    """Returns a list of all emojis."""
    emojis = []
    for filename in [f for f in os.listdir(DOCUMENT_FOLDER) if isfile(join(DOCUMENT_FOLDER, f))]:
        if filename != '.DS_Store':
            with open(join(DOCUMENT_FOLDER, filename), 'r') as document:
                emoji = pickle.load(document)
                emojis.append(emoji)
    return emojis

def write_index(schema, emojis):
    """Adds all documents to the index.

    Parameters:
    -----------
    schema - the schema for the index
    emojis - list of emoji objects
    """
    if not os.path.exists(INDEX_DIR):
        os.mkdir(INDEX_DIR)
    index = create_in(INDEX_DIR, schema)

    writer = index.writer()

    for emoji in emojis:
        print "Adding document", emoji.name
        known_as_string = ""
        for known_as in emoji.known_as:
            known_as_string += known_as[3:].replace("Emoji", "").strip() + " "

        writer.add_document(index=emoji.index,
                            name=unicode(emoji.name),
                            annotations=unicode(' '.join(emoji.annotations)),
                            related_to=unicode(' '.join(emoji.related_to)),
                            known_as=unicode(known_as_string),
                            browser=unicode(emoji.browser),
                            description=unicode(emoji.desc))

    writer.commit()

def main():
    """Main function"""
    emojis = load_emojis()
    stem_ana = StemmingAnalyzer()
    schema = Schema(index=ID(stored=True),
                    name=TEXT(analyzer=stem_ana, stored=True, field_boost=100.0),
                    annotations=KEYWORD(field_boost=50.0),
                    related_to=TEXT(analyzer=stem_ana),
                    known_as=TEXT(field_boost=50.0, analyzer=stem_ana),
                    browser=STORED,
                    description=TEXT(analyzer=stem_ana, field_boost=20.0))

    write_index(schema, emojis)

if __name__ == '__main__':
    main()
