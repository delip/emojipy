# encoding
import csv
import pywsd
import sys

from pywsd import disambiguate
from pywsd.similarity import max_similarity

from flask import request, url_for
from flask.ext.api import FlaskAPI, status, exceptions

app = FlaskAPI('emojipy')

def load_emojis(filename):
    syn_emoji = dict()
    word_emoji = dict()
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            emoji = row[0]
            text = set(row[1].split(';'))
            syns = row[2].split(';')
            for s in syns:
                syn_emoji[s] = emoji
            for t in text:
                word_emoji[t] = emoji
    return syn_emoji, word_emoji

def token_to_emoji(token_tuple):
    token = token_tuple[0]
    lemma = token_tuple[1]
    syn = token_tuple[2]
    syn_name = syn.name()
    if syn is not None and syn_name in syn_emoji:
        return syn_emoji[syn_name]
    if syn is not None:
        parent = syn.hypernym().name()
        if parent in syn_emoji:
            return syn_emoji[parent]
    if token in word_emoji:
        return word_emoji[token]
    return token

def text_to_emoji(text):
    tokens = disambiguate(text, algorithm=max_similarity, 
        similarity_option='wup', keepLemmas=True)
    return " ".join([token_to_emoji(t) for t in tokens])


@app.route("/", methods=['GET', 'POST'])
def emojipy():
    text = str(request.data.get('text', ''))
    msg = ''
    if text == '':
        text = 'i love cheesecake'
        msg = "Don't be shy. Enter some text!"
    return {
        'text': text,
        'emojid': text_to_emoji(text),
        'msg': msg
    }

reload(sys)  
sys.setdefaultencoding('utf8')
print "Server loading"
syn_emoji, word_emoji = load_emojis('emoji_mapping_sense.csv')    
print "ready"

if __name__ == "__main__":
    app.run(debug=True)
