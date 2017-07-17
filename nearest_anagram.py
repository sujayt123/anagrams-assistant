from itertools import combinations
from collections import defaultdict

def setup():
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
    return dictionary, anagrams, nearest_steals

def main():
    dictionary, anagrams, nearest_steals = setup()
    print "Welcome to the Anagrams helper! You may enter a word to find its intrinsic anagrams",
    print "and all its nearest possible 'steal-words', using the scrabble dictionary as its base."
    while(1):
        word = raw_input("Enter a word --> ").lower()
        if not word.isalpha():
            print "Your input was not a valid string!"
        elif word not in dictionary:
            print "Your input was not valid in the Scrabble Dictionary!"
        else:
            sorted_word = ''.join(sorted(word))
            print "All anagrams of '" + word + "': "
            for anagram in anagrams[sorted_word]:
                print anagram
            print ""
            print ""
            print "All nearest steals of '" + word + "', involving " + str(nearest_steals[sorted_word][0] - len(sorted_word)) + " more letters: "
            for elem in nearest_steals[sorted_word][1]:
                print anagrams[elem]
        print ""


if __name__ == "__main__":
    main()