from flask import Flask, request, render_template
from itertools import combinations
from collections import defaultdict
from pymongo import MongoClient

app = Flask(__name__)

@app.before_first_request
def setup():
    global db
    with open('config.txt') as file:
        username = file.readline().strip()
        password = file.readline().strip()
    connect_uri = "mongodb://{}:{}@ds133279.mlab.com:33279/anagram_assistant".format(username, password)
    client = MongoClient(connect_uri)
    db = client.anagram_assistant

@app.route('/', methods=['GET', 'POST'])
def website():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        global db
        word = request.form['word'].lower()
        if not word.isalpha() or db.dictionary.find_one({"word": word}) is None:
            return render_template('solution.html')
        else:
            sorted_word = ''.join(sorted(word))
            anagrams = db.anagrams.find_one({"sorted": sorted_word})['anagrams']
            steal_list = db.nearest_steals.find_one({"sorted": sorted_word})
            potential_steals = [] if steal_list is None else [
                db.anagrams.find_one({"sorted": base})['anagrams']
                for base in
                steal_list['steals'][1]
                ]
            return render_template('solution.html', valid_word=True, anagrams=anagrams, steal_words=potential_steals)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)