from collections import defaultdict
from itertools import combinations
from pymongo import MongoClient

def transform():
    dictionary = set() # set of all valid scrabble words {a, aa, ab, ad, ...}
    anagrams = defaultdict(set) # anagrams: sorted(word) --> {words}
    with open('dictionary.txt') as file:
        for line in file:
            word = line.strip().lower()
            dictionary.add(word)
            anagrams[''.join(sorted(word))].add(word)
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
    # Convert back to native python types for insertion into database
    return ([{"word": word} for word in dictionary],
            [{"sorted": k, "anagrams": list(v)} for k, v in anagrams.items()],
            [{"sorted": k, "steals": (v[0], list(v[1]))} for k, v in nearest_steals.items()]
            )

def main():
    with open('config.txt') as file:
        username = file.readline().strip()
        password = file.readline().strip()
    connect_uri = "mongodb://{}:{}@ds133279.mlab.com:33279/anagram_assistant".format(username, password)
    client = MongoClient(connect_uri)
    db = client.anagram_assistant
    db.drop_collection("dictionary")
    db.drop_collection("anagrams")
    db.drop_collection("nearest_steals")
    dictionary, anagrams, nearest_steals = transform()
    db.dictionary.insert_many(dictionary)
    db.anagrams.insert_many(anagrams)
    db.nearest_steals.insert_many(nearest_steals)

if __name__ == "__main__":
    main()