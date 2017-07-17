from flask import Flask, request, render_template
from itertools import combinations
from collections import defaultdict

app = Flask(__name__)

@app.before_first_request
def setup():
    global dictionary
    global anagrams
    global nearest_steals
    dictionary = set() # set of all valid scrabble words {a, aa, ab, ad, ...}
    anagrams = defaultdict(set) # anagrams: sorted(word) --> {words}
    with open('dictionary.txt') as file:
        for line in file:
            word = line.strip().lower()
            dictionary.add(word)
            anagrams[''.join(sorted(word))].add(word)
    #print reduce(lambda memo, y: memo if memo > len(y) else len(y), dictionary, 0)
    nearest_steals = defaultdict(lambda: [float("inf"), set()])
    for word in dictionary:
        sorted_word = ''.join(sorted(word))
        for i in range(2, len(word)):
            for subset_of_word in combinations(sorted_word, i):
                subword = ''.join(subset_of_word)
                # subset_of_word is emitted in lexicographic order
                if subword in anagrams:
                    # we have identified the subset as a valid extensible word
                    if len(word) < nearest_steals[subword][0]:
                        nearest_steals[subword][0] = len(word)
                        nearest_steals[subword][1].clear()
                    if len(word) == nearest_steals[subword][0]:
                        nearest_steals[subword][1].add(sorted_word)
    # return dictionary, anagrams, nearest_steals


@app.route('/', methods=['GET', 'POST'])
def website():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        word = request.form['word'].lower()
        if not word.isalpha() or word not in dictionary:
            return render_template('solution.html')
        else:
            sorted_word = ''.join(sorted(word))
            potential_steals = [anagrams[base] for base in nearest_steals[sorted_word][1]]
            return render_template('solution.html', valid_word=True, anagrams=anagrams[sorted_word], steal_words=potential_steals)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)